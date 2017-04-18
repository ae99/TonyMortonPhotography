# Import required django files
from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Import settings file - for media directory
from TMP import settings

# Import "Pillow" - Python image manipulation
from PIL import Image
import PIL.ExifTags


# Category class, or as Django calles it - "Model"
class Category(models.Model):
    # Defining Fields
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    # Override default save method to "slugify" name
    # "Slugifing" makes string url-safe
    # E.g. "This is a string" => "this-string"
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        # Avoid misspelt "categorys"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Photo(models.Model):
    # Define all fields
    name = models.CharField(max_length=128)

    description = models.TextField(default="", blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    original = models.CharField(max_length=128, blank=True)
    source = models.ImageField(upload_to='source')

    iso = models.CharField(max_length=128, default="", blank=True)
    lens = models.CharField(max_length=128, default="", blank=True)
    focal_length = models.CharField(max_length=128, default="", blank=True)
    exposure_time = models.CharField(max_length=128, default="", blank=True)
    date_taken = models.CharField(max_length=128, default="", blank=True)
    aperture = models.CharField(max_length=128, default="", blank=True)

    # Function to make thumbnails, accepts PIL image as input
    def make_thumb(self, img):
        img = img.copy()  # Duplicate to avoid modifying original
        img.thumbnail([400, 99999], PIL.Image.ANTIALIAS)  # Resize - max [x,y] dimensions

        # Save image to media directory, set JPEG compression quality to %55
        img.save(settings.MEDIA_DIR + "/thumb/" + str(self.id) + ".jpg", format="JPEG", quality=55)

    # Function to make web acceptable photo
    def make_web(self, img):
        img = img.copy()
        watermark = Image.open(settings.STATIC_DIR + '/watermark/watermark.png')  # Open watermark file

        # Resize image and watermark to be properly scaled
        img.thumbnail([1920, 999999], PIL.Image.ANTIALIAS)  # Max width 1920px
        watermark.thumbnail([int(min(img.size[0], img.size[1]) * 0.30), 999999], PIL.Image.ANTIALIAS)  # Resizes watermark

        imgBox = img.getbbox()
        watermarkBox = watermark.getbbox()
        margin = 10

        # Pastes the watermark onto image. Second parameter is x,y coordinate to put top-left corner of watermark
        img.paste(watermark, (imgBox[2] - margin - watermarkBox[2], imgBox[3] - margin - watermarkBox[3]), watermark)
        img.save(settings.MEDIA_DIR + "/web/" + str(self.id) + ".jpg", format="JPEG", quality=90)

    # Checks if image has been changed
    def imageChanged(self):
        if self.id is not None:
            orig = Photo.objects.get(id=self.id)
            return orig.source != self.source
        else:
            return True

    # Override default save method
    def save(self, *args, **kwargs):
        # Open Image Source
        img = Image.open(self.source)

        imageChanged = self.imageChanged()
            # Sets original filename
        if imageChanged:
            self.original = self.source.name

        # Error trapping
        try:
            # Attempt to retrieve "EXIF" Data
            # 'EXIF' is photo metadata
            raw_data = img._getexif()
            if raw_data:
                # Attempt to retrieve individual fields and set field values
                try:
                    self.iso = raw_data[34855]
                    self.lens = raw_data[42036]
                    self.focal_length = raw_data[37386][0]
                    self.exposure_time = raw_data[33434][1]
                    self.date_taken = raw_data[36867]
                    self.aperture = raw_data[33437][0] / raw_data[33437][1]
                except KeyError:
                    print("EXIF Extraction unsuccessful.")
        except AttributeError:
            print("No EXIF Data within file.")
        # Run original save method
        super(Photo, self).save(*args, **kwargs)

        # Run submethods to make web and thumbnail versions of image
        if imageChanged:
            self.make_web(img)
            self.make_thumb(img)

    def __str__(self):
        return self.name


# Runs when image is being deleted
@receiver(post_delete, sender=Photo)
def photo_post_delete_handler(sender, **kwargs):
    # Captures photo model instance - i.e. object
    photo = kwargs['instance']
    # Set variables and delete the three images - Original, Websafe and Thumbnail
    storage, path, filename = photo.source.storage, photo.source.path, str(photo.id)
    storage.delete(path)
    storage.delete(settings.MEDIA_DIR + "/web/" + filename + ".jpg")
    storage.delete(settings.MEDIA_DIR + "/thumb/" + filename + ".jpg")

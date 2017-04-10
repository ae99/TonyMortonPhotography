from django.db import models
from TMP import settings
from PIL import Image
import PIL.ExifTags
import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


def getTimeHex():
    return str(hex(int(datetime.datetime.now().timestamp())))[2:]


class Photo(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=getTimeHex)
    name = models.CharField(max_length=128)

    description = models.TextField(default="", blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    source = models.ImageField(upload_to='source')

    iso = models.CharField(max_length=128, default="", blank=True)
    lens = models.CharField(max_length=128, default="", blank=True)
    focal_length = models.CharField(max_length=128, default="", blank=True)
    exposure_time = models.CharField(max_length=128, default="", blank=True)
    takenDate = models.CharField(max_length=128, default="", blank=True)
    aperture = models.CharField(max_length=128, default="", blank=True)

    def make_thumb(self, img):
        img = img.copy()
        img.thumbnail([400, 99999], PIL.Image.ANTIALIAS)
        img.save(settings.MEDIA_DIR + "/thumb/" + self.id + ".jpg", format="JPEG", quality=60)

    def make_web(self, img):
        img = img.copy()
        watermark = Image.open(settings.STATIC_DIR + '/watermark/watermark.png')

        # Resize image and watermark to be properly scaled
        img.thumbnail([1920, 999999], PIL.Image.ANTIALIAS)
        watermark.thumbnail([int(min(img.size[0], img.size[1]) * 0.30), 999999], PIL.Image.ANTIALIAS)

        imgBox = img.getbbox()
        watermarkBox = watermark.getbbox()
        margin = 10

        # Pastes the watermark onto image. Second parameter is x,y coordinate to put top-left corner of watermark
        img.paste(watermark, (imgBox[2] - margin - watermarkBox[2], imgBox[3] - margin - watermarkBox[3]), watermark)
        img.save(settings.MEDIA_DIR + "/web/" + self.id + ".jpg", format="JPEG", quality=90)

    def save(self, *args, **kwargs):
        img = Image.open(self.source)

        try:
            raw_data = img._getexif()
            if raw_data:
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

        super(Photo, self).save(*args, **kwargs)
        self.make_web(img)
        self.make_thumb(img)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Photo)
def photo_post_delete_handler(sender, **kwargs):
    photo = kwargs['instance']
    storage, path, filename = photo.source.storage, photo.source.path, photo.id
    storage.delete(path)
    storage.delete(settings.MEDIA_DIR + "/web/" + filename + ".jpg")
    storage.delete(settings.MEDIA_DIR + "/thumb/" + filename + ".jpg")

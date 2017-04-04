from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify
from PIL import Image
import PIL.ExifTags

from TMP import settings


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(default="", blank=True)
    uploadDate = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, blank=True)

    source = models.ImageField(upload_to='source')
    filename = models.CharField(max_length=128, blank=True)

    iso = models.CharField(max_length=128, default="", blank=True)
    lens = models.CharField(max_length=128, default="", blank=True)
    focal_length = models.CharField(max_length=128, default="", blank=True)
    exposure_time = models.CharField(max_length=128, default="", blank=True)
    date_taken = models.CharField(max_length=128, default="", blank=True)
    aperture = models.CharField(max_length=128, default="", blank=True)

    def getFilename(self):
        return str(hex(int(self.uploadDate.timestamp())))[2:]

    def make_thumb(self, img, filename):
        img = img.copy()
        img.thumbnail([400, 99999], PIL.Image.ANTIALIAS)
        img.save(settings.MEDIA_DIR + "/thumb/" + filename + ".jpg", format="JPEG", quality=60)

    def make_web(self, img, filename):
        img = img.copy()
        watermark = Image.open(settings.STATIC_DIR + '/watermark/watermark.png')

        img.thumbnail([1920, 999999], PIL.Image.ANTIALIAS)

        wsize = int(min(img.size[0], img.size[1]) * 0.30)
        wpercent = (wsize / float(watermark.size[0]))
        hsize = int((float(watermark.size[1]) * float(wpercent)))

        watermark = watermark.resize((wsize, hsize), PIL.Image.ANTIALIAS)
        mbox = img.getbbox()
        sbox = watermark.getbbox()

        margin = 10
        box = (mbox[2] - sbox[2] - margin, mbox[3] - sbox[3] - margin)
        img.paste(watermark, box, watermark)

        img.save(settings.MEDIA_DIR + "/web/" + filename + ".jpg", format="JPEG", quality=90)

    def save(self, *args, **kwargs):  # Override existing save, run custom code
        self.slug = slugify(self.name)

        img = Image.open(self.source)
        
        # EXIF
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
                print("Incomplete EXIF Data")

        super(Photo, self).save(*args, **kwargs)
        self.make_web(img, self.getFilename())
        self.make_thumb(img, self.getFilename())
        self.filename = self.getFilename()
        super(Photo, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def as_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "iso": self.iso,
            "lens": self.lens,
            "focal_length": self.focal_length,
            "exposure_time": self.exposure_time,
            "aperture": self.aperture
        }

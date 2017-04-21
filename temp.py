from photos.models import Photo
for i in Photo.objects.all():
    i.make_thumb()
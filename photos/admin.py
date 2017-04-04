from django.contrib import admin


# Register your models here.
from photos.models import Tag, Photo


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Tag, TagAdmin)


admin.site.register(Photo)
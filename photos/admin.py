from django.contrib import admin
from photos.models import Category, Photo

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PhotoAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description', 'original','source' )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)

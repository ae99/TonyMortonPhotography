# Import required files
from django.contrib import admin
from photos.models import Category, Photo


# Category Admin modifications
class CategoryAdmin(admin.ModelAdmin):
    # Prepopulate "slug" field so user doesn't have to
    prepopulated_fields = {'slug': ('name',)}


# Photo Admin modifications
class PhotoAdmin(admin.ModelAdmin):
    # Add search bar for following fields
    search_fields = ('name', 'description', 'original', 'source',)


# Register Photo and Category with the Django Admin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Photo, PhotoAdmin)

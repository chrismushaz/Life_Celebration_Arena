"""Admin configuration for gallery."""

from django.contrib import admin
from .models import GalleryCategory, GalleryImage, GalleryVideo


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'uploaded_at']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description']


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

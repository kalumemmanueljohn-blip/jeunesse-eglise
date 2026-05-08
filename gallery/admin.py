from django.contrib import admin
from .models import GalleryCategory, GalleryImage, GalleryVideo

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'taken_at', 'is_featured']
    list_filter = ['category', 'is_featured']
    search_fields = ['title', 'description']

@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'uploaded_at']
    list_filter = ['category']
    search_fields = ['title', 'description']
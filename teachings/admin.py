from django.contrib import admin
from .models import Teaching, TeachingCategory

@admin.register(TeachingCategory)
class TeachingCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

@admin.register(Teaching)
class TeachingAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'category', 'content_type', 'is_featured', 'views', 'created_at']
    list_filter = ['content_type', 'category', 'is_featured']
    search_fields = ['title', 'speaker', 'description']
    readonly_fields = ['views', 'created_at']
    fieldsets = (
        ('Informations', {
            'fields': ('title', 'category', 'speaker', 'description', 'content_type', 'is_featured')
        }),
        ('Contenu', {
            'fields': ('file', 'video_url', 'external_link', 'duration')
        }),
        ('Statistiques', {
            'fields': ('views', 'created_at'),
            'classes': ('collapse',)
        }),
    )
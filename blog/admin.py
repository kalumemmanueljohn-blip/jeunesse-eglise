from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Comment

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'is_featured', 'views', 'published_at', 'preview_image']
    list_filter = ['status', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'author', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views', 'created_at', 'updated_at']
    date_hierarchy = 'published_at'
    
    def preview_image(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 10px; object-fit: cover;" />', obj.featured_image.url)
        return "—"
    preview_image.short_description = "Image"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'comment']
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approuver les commentaires"
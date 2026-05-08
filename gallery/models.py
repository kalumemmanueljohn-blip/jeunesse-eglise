from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    
    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='gallery/', verbose_name="Image")
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    taken_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de l'événement")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    def __str__(self):
        return self.title


    
class GalleryVideo(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien YouTube/Vimeo")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, verbose_name="Fichier vidéo (MP4)")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class GalleryVideo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True)  # Pour YouTube
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)  # Pour fichier MP4
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.title
from django.db import models

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='gallery/', verbose_name="Image")
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    taken_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de l'événement")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title


class GalleryVideo(models.Model):
    """Modèle unique pour les vidéos - supprimé le doublon"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien YouTube/Vimeo")
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True, verbose_name="Fichier vidéo (MP4)")
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True, verbose_name="Miniature")
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    class Meta:
        verbose_name = "Vidéo"
        verbose_name_plural = "Vidéos"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """Extrait l'ID d'une vidéo YouTube"""
        if self.video_url:
            if 'youtu.be' in self.video_url:
                return self.video_url.split('/')[-1]
            elif 'youtube.com' in self.video_url:
                return self.video_url.split('v=')[-1].split('&')[0]
        return None
    
    def get_embed_url(self):
        """Retourne l'URL embed pour YouTube"""
        video_id = self.get_video_id()
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None

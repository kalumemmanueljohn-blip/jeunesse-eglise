from django.db import models

class TeachingCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, help_text="Icône Bootstrap (ex: bi-mic)", verbose_name="Icône")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
    
    def __str__(self):
        return self.name

class Teaching(models.Model):
    TYPE_CHOICES = [
        ('audio', '🎵 Audio'),
        ('video', '🎥 Vidéo'),
        ('pdf', '📄 PDF'),
        ('text', '📝 Texte'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    category = models.ForeignKey(TeachingCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='teachings', verbose_name="Catégorie")
    speaker = models.CharField(max_length=100, verbose_name="Prédicateur/Enseignant")
    description = models.TextField(verbose_name="Description")
    content_type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Type de contenu")
    file = models.FileField(upload_to='teachings/', blank=True, null=True, verbose_name="Fichier")
    video_url = models.URLField(blank=True, null=True, verbose_name="Lien YouTube/Vimeo")
    external_link = models.URLField(blank=True, null=True, verbose_name="Lien externe")
    duration = models.CharField(max_length=20, blank=True, help_text="ex: 34min", verbose_name="Durée")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, verbose_name="Vues")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Enseignement"
        verbose_name_plural = "Enseignements"
    
    def __str__(self):
        return self.title
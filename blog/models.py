from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True, verbose_name="URL personnalisée")
    excerpt = models.TextField(max_length=300, verbose_name="Résumé")
    content = models.TextField(verbose_name="Contenu")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Image à la une")
    author = models.CharField(max_length=100, verbose_name="Auteur")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    tags = models.CharField(max_length=200, blank=True, help_text="Séparés par des virgules", verbose_name="Tags")
    views = models.IntegerField(default=0, verbose_name="Vues")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Date de publication")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = "Article"
        verbose_name_plural = "Articles"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments', verbose_name="Article")
    name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email", blank=True)
    comment = models.TextField(verbose_name="Commentaire")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
    
    def __str__(self):
        return f"{self.name} - {self.post.title}"
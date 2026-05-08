from django.db import models

class VerseOfTheDay(models.Model):
    verse = models.TextField(verbose_name="Verset")
    reference = models.CharField(max_length=100, verbose_name="Référence")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Verset du jour"
        verbose_name_plural = "Versets du jour"
    
    def __str__(self):
        return self.reference

class Testimonial(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    message = models.TextField(verbose_name="Témoignage")
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True, verbose_name="Photo")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
    
    def __str__(self):
        return self.name
    
class Subscriber(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")
    name = models.CharField(max_length=100, blank=True, verbose_name="Nom")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Abonné"
        verbose_name_plural = "Abonnés"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.phone_number} - {self.created_at.strftime('%d/%m/%Y')}"
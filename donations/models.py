from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('confirmed', 'Confirmé'),
        ('failed', 'Échoué'),
    ]
    
    PAYMENT_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('airtel', 'Airtel Money'),
        ('orange', 'Orange Money'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilisateur")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name="Moyen de paiement")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Numéro de téléphone")
    transaction_id = models.CharField(max_length=100, blank=True, verbose_name="ID Transaction")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    message = models.TextField(blank=True, verbose_name="Message")
    anonymous = models.BooleanField(default=False, verbose_name="Don anonyme")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Don"
        verbose_name_plural = "Dons"
    
    def __str__(self):
        if self.user and not self.anonymous:
            return f"{self.user.username} - {self.amount}€"
        return f"Anonyme - {self.amount}€"
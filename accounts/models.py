from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    # Types de membres
    MEMBER_TYPE_CHOICES = [
        ('staff', '👑 Membre du Staff'),
        ('regular', '🙏 Jeune de l\'église'),
        ('guest', '👤 Invité'),
    ]
    
    # Départements
    DEPARTMENT_CHOICES = [
        ('coordination', '🎯 Coordination'),
        ('evangelisation', '📢 Évangélisation'),
        ('louange', '🎵 Louange'),
        ('enseignement', '📖 Enseignement'),
        ('technique', '💻 Technique / Médias'),
        ('communication', '📱 Communication'),
        ('accueil', '🤝 Accueil'),
        ('priere', '🙏 Prière'),
        ('social', '❤️ Action sociale'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    address = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    church = models.CharField(max_length=100, blank=True, verbose_name="Église d'origine")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Date de naissance")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Photo de profil")
    bio = models.TextField(blank=True, max_length=500, verbose_name="Biographie")
    
    # Nouveaux champs
    member_type = models.CharField(max_length=20, choices=MEMBER_TYPE_CHOICES, default='guest', verbose_name="Type de membre")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, blank=True, null=True, verbose_name="Département")
    is_regular_member = models.BooleanField(default=False, verbose_name="Prie déjà dans notre église")
    
    is_leader = models.BooleanField(default=False, verbose_name="Leader du groupe")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        member_type_display = dict(self.MEMBER_TYPE_CHOICES).get(self.member_type, '')
        if self.member_type == 'staff' and self.department:
            return f"{self.user.username} - {member_type_display} ({self.get_department_display()})"
        return f"{self.user.username} - {member_type_display}"
    
    def get_member_badge(self):
        if self.member_type == 'staff':
            return f'<span class="badge-staff">👑 Staff - {self.get_department_display()}</span>'
        elif self.member_type == 'regular':
            return '<span class="badge-regular">🙏 Membre régulier</span>'
        else:
            return '<span class="badge-guest">👤 Invité</span>'

# ============================================
# SIGNALS
# ============================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée un profil utilisateur automatiquement à l'inscription"""
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil quand l'utilisateur est sauvegardé"""
    try:
        instance.profile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)

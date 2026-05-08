from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator

# ============================================
# CONVERSATION
# ============================================

class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations', verbose_name="Participants")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    is_group = models.BooleanField(default=False, verbose_name="Groupe")
    group_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom du groupe")
    group_avatar = models.ImageField(upload_to='group_avatars/', blank=True, null=True, verbose_name="Avatar du groupe")
    group_description = models.TextField(blank=True, verbose_name="Description du groupe")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_groups')
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
    
    def __str__(self):
        if self.is_group:
            return self.group_name or f"Groupe {self.id}"
        else:
            participants = list(self.participants.all()[:2])
            if len(participants) == 2:
                return f"{participants[0].username} & {participants[1].username}"
            return f"Conversation {self.id}"
    
    def get_other_participant(self, user):
        """Retourne l'autre participant dans une conversation privée"""
        if self.is_group:
            return None
        return self.participants.exclude(id=user.id).first()
    
    def get_display_name(self, user=None):
        """Retourne le nom à afficher pour cette conversation"""
        if self.is_group:
            return self.group_name or f"Groupe {self.id}"
        else:
            other = self.get_other_participant(user) if user else None
            if other:
                return other.get_full_name() or other.username
            return "Conversation"
    
    def get_avatar(self, user=None):
        """Retourne l'avatar de la conversation"""
        if self.is_group and self.group_avatar:
            return self.group_avatar.url
        else:
            other = self.get_other_participant(user) if user else None
            if other and hasattr(other, 'profile') and other.profile.avatar:
                return other.profile.avatar.url
        return None
    
    # ⭐⭐⭐ METHODE POUR LE DERNIER MESSAGE ⭐⭐⭐
    def last_message(self):
        """Retourne le dernier message de la conversation"""
        return self.messages.filter(is_deleted=False).first()
    
    # ⭐⭐⭐ METHODE POUR LE NOMBRE DE MESSAGES NON LUS ⭐⭐⭐
    def unread_count(self, user):
        """Retourne le nombre de messages non lus pour un utilisateur"""
        return self.messages.filter(is_read=False).exclude(sender=user).count()
    
    def messages_count(self):
        """Retourne le nombre total de messages"""
        return self.messages.filter(is_deleted=False).count()


# ============================================
# MESSAGE
# ============================================

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name="Conversation")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Expéditeur")
    content = models.TextField(verbose_name="Contenu", blank=True)
    file = models.FileField(
        upload_to='chat_files/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name="Fichier joint",
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mp3', 'wav', 'webm', 'ogg', 'm4a', 'pdf'])]
    )
    file_name = models.CharField(max_length=255, blank=True, verbose_name="Nom du fichier")
    file_size = models.IntegerField(default=0, verbose_name="Taille du fichier (bytes)")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="Lu le")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Envoyé le")
    edited_at = models.DateTimeField(blank=True, null=True, verbose_name="Modifié le")
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")
    deleted_at = models.DateTimeField(blank=True, null=True, verbose_name="Supprimé le")
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Message"
        verbose_name_plural = "Messages"
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:30] if self.content else '[Fichier]'}"
    
    def mark_as_read(self):
        """Marquer le message comme lu"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])
    
    def soft_delete(self):
        """Supprimer le message (soft delete)"""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.content = ""
        self.file = None
        self.save(update_fields=['is_deleted', 'deleted_at', 'content', 'file'])
    
    def get_file_type(self):
        """Retourne le type de fichier pour l'affichage"""
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            image_exts = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg']
            video_exts = ['mp4', 'mov', 'avi', 'mkv', 'webm']
            audio_exts = ['mp3', 'wav', 'ogg', 'm4a', 'aac', 'flac', 'webm']
            pdf_exts = ['pdf']
            doc_exts = ['doc', 'docx', 'txt', 'rtf']
            print(f"DEBUG - Fichier: {self.file.name}, Extension: {ext}")
            if ext in image_exts:
                return 'image'
            elif ext in video_exts:
                return 'video'
            elif ext in audio_exts:
                return 'audio'
            elif ext in pdf_exts:
                return 'pdf'
            elif ext in doc_exts:
                return 'document'
        return None


# ============================================
# STATUT UTILISATEUR (EN LIGNE / HORS LIGNE)
# ============================================

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chat_status', verbose_name="Utilisateur")
    is_online = models.BooleanField(default=False, verbose_name="En ligne")
    last_seen = models.DateTimeField(default=timezone.now, verbose_name="Dernière vue")
    typing_in = models.ForeignKey(Conversation, on_delete=models.SET_NULL, null=True, blank=True, related_name='typing_users')
    
    class Meta:
        verbose_name = "Statut utilisateur"
        verbose_name_plural = "Statuts utilisateurs"
    
    def __str__(self):
        status = "🟢 En ligne" if self.is_online else f"⚫ Vu à {self.last_seen.strftime('%H:%M')}"
        return f"{self.user.username} - {status}"
    
    def update_online_status(self, is_online):
        """Mettre à jour le statut en ligne"""
        self.is_online = is_online
        if not is_online:
            self.last_seen = timezone.now()
        self.save()


# ============================================
# RÉACTIONS AUX MESSAGES (👍, ❤️, etc.)
# ============================================

class MessageReaction(models.Model):
    REACTION_CHOICES = [
        ('👍', '👍 Like'),
        ('❤️', '❤️ Love'),
        ('😂', '😂 Laugh'),
        ('😮', '😮 Wow'),
        ('😢', '😢 Sad'),
        ('🙏', '🙏 Pray'),
        ('🔥', '🔥 Fire'),
        ('👏', '👏 Bravo'),
    ]
    
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions', verbose_name="Message")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_reactions', verbose_name="Utilisateur")
    reaction = models.CharField(max_length=10, choices=REACTION_CHOICES, verbose_name="Réaction")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Réagi le")
    
    class Meta:
        unique_together = ['message', 'user']
        verbose_name = "Réaction"
        verbose_name_plural = "Réactions"
    
    def __str__(self):
        return f"{self.user.username}: {self.reaction}"


# ============================================
# SIGNAL POUR CRÉER AUTOMATIQUEMENT LE STATUT
# ============================================

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    """Crée automatiquement un statut pour chaque nouvel utilisateur"""
    if created:
        UserStatus.objects.get_or_create(user=instance)


@receiver(post_save, sender=Message)
def update_conversation_timestamp(sender, instance, created, **kwargs):
    """Met à jour le timestamp de la conversation quand un message est envoyé"""
    if created:
        conversation = instance.conversation
        conversation.updated_at = timezone.now()
        conversation.save(update_fields=['updated_at'])
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Conversation, Message, UserStatus, MessageReaction

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_name', 'is_group', 'participants_count', 'messages_count', 'unread_count', 'updated_at']
    list_filter = ['is_group', 'created_at', 'updated_at']
    filter_horizontal = ['participants']
    search_fields = ['group_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def display_name(self, obj):
        if obj.is_group:
            return f"👥 {obj.group_name}" if obj.group_name else f"👥 Groupe {obj.id}"
        else:
            return "👤 Conversation privée"
    display_name.short_description = "Nom"
    
    def participants_count(self, obj):
        return obj.participants.count()
    participants_count.short_description = "Participants"
    
    def messages_count(self, obj):
        count = obj.messages.count()
        return format_html('<span style="color: #3498db;">📨 {}</span>', count)
    messages_count.short_description = "Messages"
    
    def unread_count(self, obj):
        return obj.messages.filter(is_read=False).count()
    unread_count.short_description = "Non lus"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'conversation_display', 'content_preview', 'has_file', 'is_read', 'created_at']
    list_filter = ['is_read', 'is_deleted', 'created_at']
    search_fields = ['sender__username', 'content']
    readonly_fields = ['created_at', 'read_at', 'edited_at']
    
    def conversation_display(self, obj):
        if obj.conversation.is_group:
            return obj.conversation.group_name or f"Groupe {obj.conversation.id}"
        else:
            participants = obj.conversation.participants.all()
            return " & ".join([p.username for p in participants[:2]])
    conversation_display.short_description = "Conversation"
    
    def content_preview(self, obj):
        if obj.is_deleted:
            return format_html('<span style="color: #95a5a6;">🗑️ [Message supprimé]</span>')
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Message"
    
    def has_file(self, obj):
        if obj.file:
            return format_html('<span style="color: #27ae60;">📎 {}</span>', obj.file_name or "Fichier")
        return "—"
    has_file.short_description = "Pièce jointe"

@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'status_badge', 'last_seen']
    list_filter = ['is_online', 'last_seen']
    search_fields = ['user__username']
    readonly_fields = ['last_seen']
    
    def status_badge(self, obj):
        if obj.is_online:
            return format_html('<span style="color: #2ecc71;">🟢 En ligne</span>')
        elif obj.last_seen:
            return format_html('<span style="color: #95a5a6;">⚫ Vu à {}</span>', obj.last_seen.strftime('%H:%M'))
        return format_html('<span style="color: #95a5a6;">⚫ Hors ligne</span>')
    status_badge.short_description = "Statut"

@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'reaction', 'created_at']
    list_filter = ['reaction', 'created_at']
    search_fields = ['user__username', 'message__content']
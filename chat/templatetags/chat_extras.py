from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def conversation_name(conversation, user):
    """Retourne le nom de la conversation pour l'utilisateur"""
    if not conversation:
        return "Conversation"
    
    if conversation.is_group:
        return conversation.group_name or f"Groupe {conversation.id}"
    
    other = conversation.get_other_participant(user) if hasattr(conversation, 'get_other_participant') else None
    if other:
        return other.get_full_name() or other.username
    return "Conversation"

@register.filter
def conversation_avatar(conversation, user):
    """Retourne l'avatar de la conversation"""
    if not conversation:
        return None
    
    if conversation.is_group and conversation.group_avatar:
        return conversation.group_avatar.url
    
    other = conversation.get_other_participant(user) if hasattr(conversation, 'get_other_participant') else None
    if other and hasattr(other, 'profile') and other.profile and other.profile.avatar:
        return other.profile.avatar.url
    return None

@register.simple_tag
def message_reactions_json(message):
    """Retourne les réactions d'un message en JSON"""
    if not message or not hasattr(message, 'reactions'):
        return mark_safe('{}')
    
    reactions = {}
    for r in message.reactions.all():
        reactions[r.user.username] = r.reaction
    return mark_safe(json.dumps(reactions))

@register.filter
def time_ago(date):
    """Retourne le temps écoulé depuis la date"""
    from django.utils import timezone
    
    if not date:
        return ""
    
    now = timezone.now()
    diff = now - date
    
    if diff.days > 30:
        return date.strftime('%d/%m/%Y')
    elif diff.days > 0:
        return f"{diff.days}j"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}h"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}m"
    else:
        return "à l'instant"

@register.filter
def truncatechars_custom(value, arg):
    """Tronque un texte après un certain nombre de caractères"""
    if not value:
        return ""
    
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if len(value) <= length:
        return value
    return value[:length] + "..."

@register.filter
def get_item(dictionary, key):
    """Récupère un élément d'un dictionnaire par sa clé"""
    if not dictionary:
        return None
    return dictionary.get(key)
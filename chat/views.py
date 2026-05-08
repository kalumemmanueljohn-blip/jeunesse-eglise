from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Conversation, Message, UserStatus, MessageReaction
import json
import os

# ============================================
# VUES PRINCIPALES
# ============================================

@login_required
def inbox(request):
    """Liste des conversations de l'utilisateur"""
    conversations = request.user.conversations.all().order_by('-updated_at')
    
    status, created = UserStatus.objects.get_or_create(user=request.user)
    status.is_online = True
    status.last_seen = timezone.now()
    status.save()
    
    context = {
        'conversations': conversations,
    }
    return render(request, 'chat/inbox.html', context)


@login_required
def conversation_detail(request, user_id):
    """Conversation avec un utilisateur spécifique"""
    other_user = get_object_or_404(User, id=user_id)
    
    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(participants=other_user).filter(is_group=False).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
    
    # Marquer les messages comme lus
    unread_messages = conversation.messages.filter(is_read=False).exclude(sender=request.user)
    for msg in unread_messages:
        msg.mark_as_read()
    
    messages_list = conversation.messages.filter(is_deleted=False).order_by('created_at')
    paginator = Paginator(messages_list, 50)
    page = request.GET.get('page', 1)
    messages_page = paginator.get_page(page)
    
    context = {
        'conversation': conversation,
        'other_user': other_user,
        'messages': messages_page,
    }
    return render(request, 'chat/conversation.html', context)


@login_required
def new_message(request):
    """Page pour démarrer une nouvelle conversation"""
    conversations = request.user.conversations.all().order_by('-updated_at')[:10]
    return render(request, 'chat/new_message.html', {'conversations': conversations})


# ============================================
# API ENDPOINTS
# ============================================

@login_required
@require_POST
def send_message(request, conversation_id):
    """Envoyer un message (texte ou fichier)"""
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
        content = request.POST.get('content', '').strip()
        file = request.FILES.get('file')
        
        if not content and not file:
            return JsonResponse({'error': 'Message vide'}, status=400)
        
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content if content else ""
        )
        
        if file:
            # Vérifier la taille (max 20MB)
            if file.size > 50 * 1024 * 1024:  # 50 MB
                 return JsonResponse({'error': 'Fichier trop volumineux (max 50MB)'}, status=400)
            
            # Vérifier l'extension
            file_extension = file.name.split('.')[-1].lower()
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'mp4', 'mp3', 'wav', 'webm', 'pdf', 'doc', 'docx', 'txt']
            
            if file_extension not in allowed_extensions:
                return JsonResponse({'error': f'Type de fichier non autorisé: {file_extension}'}, status=400)
            
            message.file = file
            message.file_name = file.name
            message.file_size = file.size
            message.save()
        
        conversation.updated_at = timezone.now()
        conversation.save(update_fields=['updated_at'])
        
        response_data = {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'sender_id': message.sender.id,
            'created_at': message.created_at.strftime('%H:%M'),
            'is_read': message.is_read,
            'file_url': message.file.url if message.file else None,
            'file_name': message.file_name if message.file else None,
            'file_type': message.get_file_type() if message.file else None,
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def mark_read(request, message_id):
    """Marquer un message comme lu"""
    try:
        message = get_object_or_404(Message, id=message_id, conversation__participants=request.user)
        if message.sender != request.user:
            message.mark_as_read()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
@require_POST
def add_reaction(request, message_id):
    """Ajouter une réaction à un message"""
    message = get_object_or_404(Message, id=message_id)
    reaction = request.POST.get('reaction')
    
    valid_reactions = ['👍', '❤️', '😂', '😮', '😢', '🙏', '🔥', '👏']
    if reaction not in valid_reactions:
        return JsonResponse({'error': 'Réaction invalide'}, status=400)
    
    obj, created = MessageReaction.objects.update_or_create(
        message=message,
        user=request.user,
        defaults={'reaction': reaction}
    )
    
    reactions = {}
    for r in message.reactions.all():
        reactions[r.user.username] = r.reaction
    
    return JsonResponse({'status': 'ok', 'reactions': reactions})


@login_required
@require_POST
def delete_message(request, message_id):
    """Supprimer un message (soft delete)"""
    try:
        message = get_object_or_404(Message, id=message_id, sender=request.user)
        message.is_deleted = True
        message.content = "[Message supprimé]"
        message.file = None
        message.save()
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def user_status(request):
    """Récupérer le statut de plusieurs utilisateurs"""
    user_ids = request.GET.get('user_ids', '').split(',')
    statuses = {}
    
    for user_id in user_ids:
        if user_id and user_id.isdigit():
            try:
                status = UserStatus.objects.get(user_id=user_id)
                # Vérifier si l'utilisateur a été actif dans les dernières 2 minutes
                from django.utils import timezone
                from datetime import timedelta
                
                is_online = status.is_online
                if status.last_seen and (timezone.now() - status.last_seen) > timedelta(minutes=2):
                    is_online = False
                    # Mettre à jour le statut hors ligne automatiquement
                    if status.is_online:
                        status.is_online = False
                        status.save()
                
                statuses[user_id] = {
                    'is_online': is_online,
                    'last_seen': status.last_seen.strftime('%H:%M') if not is_online else None,
                }
            except UserStatus.DoesNotExist:
                statuses[user_id] = {'is_online': False, 'last_seen': None}
    
    return JsonResponse(statuses)


@login_required
@require_POST
def update_online_status(request):
    """Mettre à jour le statut en ligne"""
    try:
        data = json.loads(request.body)
        is_online = data.get('is_online', False)
        
        status, created = UserStatus.objects.get_or_create(user=request.user)
        status.is_online = is_online
        if not is_online:
            status.last_seen = timezone.now()
        status.save()
        
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def search_users(request):
    """API de recherche d'utilisateurs"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'users': []})
    
    users = User.objects.filter(
        models.Q(username__icontains=query) |
        models.Q(first_name__icontains=query) |
        models.Q(last_name__icontains=query) |
        models.Q(email__icontains=query)
    ).exclude(id=request.user.id)[:15]
    
    users_data = []
    for user in users:
        conversation = Conversation.objects.filter(
            participants=request.user
        ).filter(participants=user).filter(is_group=False).first()
        
        users_data.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'avatar': user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None,
            'conversation_id': conversation.id if conversation else None,
        })
    
    return JsonResponse({'users': users_data})


@login_required
def get_messages(request, conversation_id):
    """API pour récupérer les messages"""
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    
    messages_qs = conversation.messages.filter(is_deleted=False).order_by('-created_at')[:50]
    
    messages_data = []
    for msg in reversed(messages_qs):
        msg_data = {
            'id': msg.id,
            'content': msg.content,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.username,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_read': msg.is_read,
            'file_url': msg.file.url if msg.file else None,
            'file_name': msg.file_name if msg.file else None,
            'file_type': msg.get_file_type() if msg.file else None,
        }
        messages_data.append(msg_data)
    
    return JsonResponse({'messages': messages_data})


@login_required
@require_POST
def mark_multiple_read(request):
    """Marquer plusieurs messages comme lus"""
    try:
        data = json.loads(request.body)
        message_ids = data.get('message_ids', [])
        
        for message_id in message_ids:
            try:
                message = Message.objects.get(id=message_id, conversation__participants=request.user)
                if message.sender != request.user:
                    message.mark_as_read()
            except Message.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
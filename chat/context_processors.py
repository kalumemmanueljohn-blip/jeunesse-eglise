from .models import Message, Conversation # type: ignore

def unread_messages_count(request):
    """Context processor pour le nombre de messages non lus"""
    if request.user.is_authenticated:
        try:
            conversations = request.user.conversations.all()
            total_unread = sum(conv.unread_count(request.user) for conv in conversations)
            return {'unread_messages_count': total_unread}
        except:
            return {'unread_messages_count': 0}
    return {'unread_messages_count': 0}
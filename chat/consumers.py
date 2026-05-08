import json
from time import timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversation, Message, UserStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        self.room_name = f'user_{self.user.id}'
        self.room_group_name = f'chat_{self.room_name}'
        
        # Rejoindre le groupe personnel
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Marquer comme en ligne
        await self.set_user_online(True)
    
    async def disconnect(self, close_code):
        # Quitter le groupe
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Marquer comme hors ligne
        await self.set_user_online(False)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'message':
            await self.handle_message(data)
        elif message_type == 'typing':
            await self.handle_typing(data)
        elif message_type == 'read':
            await self.handle_read(data)
    
    async def handle_message(self, data):
        conversation_id = data.get('conversation_id')
        content = data.get('content', '')
        
        if not content and not data.get('file_url'):
            return
        
        # Sauvegarder le message
        message = await self.save_message(
            conversation_id, 
            self.user.id, 
            content,
            data.get('file_url'),
            data.get('file_name')
        )
        
        if message:
            # Obtenir les participants
            participants = await self.get_conversation_participants(conversation_id)
            
            message_data = {
                'id': message['id'],
                'content': message['content'],
                'sender_id': self.user.id,
                'sender_name': self.user.username,
                'conversation_id': conversation_id,
                'created_at': message['created_at'],
                'file_url': message.get('file_url'),
                'file_name': message.get('file_name'),
                'file_type': message.get('file_type'),
            }
            
            # Envoyer à tous les participants sauf l'expéditeur
            for participant_id in participants:
                if participant_id != self.user.id:
                    await self.channel_layer.group_send(
                        f'chat_user_{participant_id}',
                        {
                            'type': 'chat_message',
                            'message': message_data
                        }
                    )
            
            # Confirmation à l'expéditeur
            await self.send(text_data=json.dumps({
                'type': 'message_sent',
                'message': message_data
            }))
    
    async def handle_typing(self, data):
        conversation_id = data.get('conversation_id')
        is_typing = data.get('is_typing', False)
        
        participants = await self.get_conversation_participants(conversation_id)
        
        for participant_id in participants:
            if participant_id != self.user.id:
                await self.channel_layer.group_send(
                    f'chat_user_{participant_id}',
                    {
                        'type': 'typing_indicator',
                        'user_id': self.user.id,
                        'user_name': self.user.username,
                        'conversation_id': conversation_id,
                        'is_typing': is_typing
                    }
                )
    
    async def handle_read(self, data):
        message_ids = data.get('message_ids', [])
        for message_id in message_ids:
            await self.mark_message_as_read(message_id, self.user.id)
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'data': event['message']
        }))
    
    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'data': {
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'conversation_id': event['conversation_id'],
                'is_typing': event['is_typing']
            }
        }))
    
    @database_sync_to_async
    def set_user_online(self, is_online):
        status, created = UserStatus.objects.get_or_create(user=self.user)
        status.is_online = is_online
        if not is_online:
            status.last_seen = timezone.now()
        status.save()
    
    @database_sync_to_async
    def save_message(self, conversation_id, user_id, content, file_url, file_name):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            user = User.objects.get(id=user_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=user,
                content=content
            )
            conversation.updated_at = timezone.now()
            conversation.save()
            
            return {
                'id': message.id,
                'content': message.content,
                'created_at': message.created_at.strftime('%H:%M'),
                'file_url': message.file.url if message.file else None,
                'file_name': message.file_name,
                'file_type': message.get_file_type(),
            }
        except Exception as e:
            print(f"Error saving message: {e}")
            return None
    
    @database_sync_to_async
    def get_conversation_participants(self, conversation_id):
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            return list(conversation.participants.values_list('id', flat=True))
        except Exception:
            return []
    
    @database_sync_to_async
    def mark_message_as_read(self, message_id, user_id):
        try:
            message = Message.objects.get(id=message_id)
            if message.sender.id != user_id:
                message.mark_as_read()
            return True
        except Exception:
            return False
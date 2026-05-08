from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Pages principales
    path('', views.inbox, name='inbox'),
    path('conversation/<int:user_id>/', views.conversation_detail, name='conversation'),
    path('new/', views.new_message, name='new_message'),
    
    # API endpoints
    path('api/send/<int:conversation_id>/', views.send_message, name='send_message'),
    path('api/read/<int:message_id>/', views.mark_read, name='mark_read'),
    path('api/reaction/<int:message_id>/', views.add_reaction, name='add_reaction'),
    path('api/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('api/status/', views.user_status, name='user_status'),
    path('api/online-status/', views.update_online_status, name='update_online_status'),
    path('api/search/', views.search_users, name='search_users'),
    path('api/messages/<int:conversation_id>/', views.get_messages, name='get_messages'),
    path('api/mark-multiple-read/', views.mark_multiple_read, name='mark_multiple_read'),
]
# events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # Pages publiques
    path('', views.events_list, name='events_list'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('<int:id>/register/', views.register_event, name='register_event'),
    
    # Pages ADMIN (protégées par les vues)
    path('add/', views.add_event, name='add_event'),
    path('manage/', views.events_manage, name='events_manage'),
    path('<int:id>/edit/', views.event_edit, name='event_edit'),
    path('<int:id>/delete/', views.delete_event, name='event_delete'),
]

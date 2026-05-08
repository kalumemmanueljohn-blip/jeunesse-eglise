from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('<int:id>/register/', views.register_event, name='register_event'),
    path('<int:id>/delete/', views.delete_event, name='delete_event'),
    path('add/', views.add_event, name='add_event'),  # ← Ajouter cette ligne
    path('<int:id>/register/', views.register_event, name='register_event'),
]
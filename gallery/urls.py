from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('photo/ajouter/', views.add_photo, name='add_photo'),
    path('video/ajouter/', views.add_video, name='add_video'),
    path('photo/supprimer/<int:id>/', views.delete_photo, name='delete_photo'),
    path('video/supprimer/<int:id>/', views.delete_video, name='delete_video'),
]
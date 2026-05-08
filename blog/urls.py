from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog'),
    path('ajouter/', views.add_blog, name='add_blog'),
    path('supprimer/<slug:slug>/', views.delete_blog, name='delete_blog'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
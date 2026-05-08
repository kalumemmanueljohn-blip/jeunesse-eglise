from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachings, name='teachings'),
    path('ajouter/', views.add_teaching, name='add_teaching'),
    path('<int:id>/delete/', views.delete_teaching, name='delete_teaching'),
]
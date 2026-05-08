from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('save-phone/', views.save_phone, name='save_phone'),
     path('subscribers/', views.subscribers_list, name='subscribers_list'),
    path('subscriber/toggle/<int:id>/', views.subscriber_toggle, name='subscriber_toggle'),
    path('subscriber/delete/<int:id>/', views.subscriber_delete, name='subscriber_delete'),
    path('subscribers/export/', views.export_subscribers_csv, name='export_subscribers_csv'),
]
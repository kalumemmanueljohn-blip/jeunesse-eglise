from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('delete/', views.delete_account, name='delete_account'),  # ← AJOUTER CETTE LIGNE
     path('manage/', views.manage_users, name='manage_users'),
    path('toggle-status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('toggle-staff/<int:user_id>/', views.toggle_user_staff, name='toggle_user_staff'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('make-superuser/<int:user_id>/', views.make_superuser, name='make_superuser'),
    path('api/user/<int:user_id>/', views.api_user_detail, name='api_user_detail'),
]

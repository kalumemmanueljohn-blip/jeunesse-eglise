from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from events.models import Participant
from donations.models import Donation
from .models import UserProfile
from .forms import CustomUserCreationForm  # ← IMPORTER LE FORMULAIRE PERSONNALISÉ
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from django.db import models

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # ← UTILISER LE FORMULAIRE PERSONNALISÉ
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} ! Votre compte a été créé avec succès.")
            return redirect('dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()  # ← UTILISER LE FORMULAIRE PERSONNALISÉ
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bon retour {user.username} !")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')

@login_required
def dashboard(request):
    my_events = Participant.objects.filter(user=request.user).select_related('event').order_by('-registered_at')
    my_donations = Donation.objects.filter(user=request.user, status='confirmed')[:5]
    profile = request.user.profile
    
    context = {
        'my_events': my_events,
        'my_donations': my_donations,
        'profile': profile,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        # Mettre à jour l'utilisateur
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Mettre à jour le profil
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        profile.church = request.POST.get('church', '')
        profile.bio = request.POST.get('bio', '')
        
        # Mettre à jour les nouveaux champs
        profile.member_type = request.POST.get('member_type', profile.member_type)
        profile.department = request.POST.get('department', '')
        profile.is_regular_member = request.POST.get('is_regular_member') == 'on'
        
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        # Si membre du staff, mettre à jour is_staff
        if profile.member_type == 'staff':
            request.user.is_staff = True
        else:
            request.user.is_staff = False
        request.user.save()
        
        messages.success(request, "Votre profil a été mis à jour !")
        return redirect('dashboard')
    
    return render(request, 'accounts/profile_edit.html', {'profile': profile})

@login_required
def delete_account(request):
    """Supprimer définitivement le compte de l'utilisateur"""
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        
        # Vérifier le mot de passe
        user = authenticate(request, username=request.user.username, password=password)
        if not user:
            messages.error(request, "Mot de passe incorrect.")
            return redirect('delete_account')
        
        # Vérifier la confirmation
        if confirmation != 'SUPPRIMER':
            messages.error(request, 'Veuillez taper "SUPPRIMER" pour confirmer la suppression.')
            return redirect('delete_account')
        
        # Supprimer le compte
        username = request.user.username
        request.user.delete()
        messages.success(request, f'Votre compte "{username}" a été supprimé avec succès.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')

@staff_member_required
def manage_users(request):
    """Page d'administration des utilisateurs (réservée aux staff)"""
    
    # Récupérer tous les utilisateurs
    users_list = User.objects.all().order_by('-date_joined')
    
    # Filtres
    search = request.GET.get('search', '')
    role = request.GET.get('role', '')
    status = request.GET.get('status', '')
    
    if search:
        users_list = users_list.filter(
            models.Q(username__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search)
        )
    
    if role == 'staff':
        users_list = users_list.filter(is_staff=True)
    elif role == 'admin':
        users_list = users_list.filter(is_superuser=True)
    elif role == 'user':
        users_list = users_list.filter(is_staff=False, is_superuser=False)
    
    if status == 'active':
        users_list = users_list.filter(is_active=True)
    elif status == 'inactive':
        users_list = users_list.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(users_list, 20)
    page_number = request.GET.get('page', 1)
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search': search,
        'role': role,
        'status': status,
        'total_users': User.objects.count(),
        'total_staff': User.objects.filter(is_staff=True).count(),
        'total_active': User.objects.filter(is_active=True).count(),
    }
    return render(request, 'accounts/manage_users.html', context)

@staff_member_required
def toggle_user_status(request, user_id):
    """Activer/Désactiver un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, f'✅ Utilisateur {user.username} {"activé" if user.is_active else "désactivé"}')
    return redirect('manage_users')

@staff_member_required
def toggle_user_staff(request, user_id):
    """Rendre utilisateur staff ou non"""
    user = get_object_or_404(User, id=user_id)
    # Ne pas modifier les superusers
    if not user.is_superuser:
        user.is_staff = not user.is_staff
        user.save()
        messages.success(request, f'✅ Utilisateur {user.username} est maintenant {"staff" if user.is_staff else "utilisateur normal"}')
    else:
        messages.warning(request, f'⚠️ Impossible de modifier un superutilisateur')
    return redirect('manage_users')

@staff_member_required
def delete_user(request, user_id):
    """Supprimer un utilisateur"""
    user = get_object_or_404(User, id=user_id)
    # Ne pas supprimer soi-même
    if user == request.user:
        messages.error(request, '❌ Vous ne pouvez pas supprimer votre propre compte depuis cette page.')
        return redirect('manage_users')
    
    username = user.username
    user.delete()
    messages.success(request, f'✅ Utilisateur "{username}" supprimé avec succès')
    return redirect('manage_users')

@staff_member_required
def make_superuser(request, user_id):
    """Promouvoir un utilisateur en superutilisateur"""
    user = get_object_or_404(User, id=user_id)
    if user == request.user:
        messages.warning(request, '⚠️ Vous êtes déjà superutilisateur')
    else:
        user.is_superuser = True
        user.is_staff = True
        user.save()
        messages.success(request, f'✅ {user.username} est maintenant superutilisateur')
    return redirect('manage_users')

@staff_member_required
def api_user_detail(request, user_id):
    """API pour récupérer les détails d'un utilisateur (AJAX)"""
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    
    data = {
        'id': user.id,
        'username': user.username,
        'full_name': user.get_full_name(),
        'email': user.email,
        'phone': profile.phone_number if hasattr(profile, 'phone_number') else '',
        'date_joined': user.date_joined.strftime('%d/%m/%Y'),
        'member_type': dict(profile.MEMBER_TYPE_CHOICES).get(profile.member_type, 'Membre') if hasattr(profile, 'member_type') else 'Membre',
        'department': profile.get_department_display() if hasattr(profile, 'get_department_display') and profile.department else '',
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'avatar': profile.avatar.url if hasattr(profile, 'avatar') and profile.avatar else None,
    }
    return JsonResponse(data)
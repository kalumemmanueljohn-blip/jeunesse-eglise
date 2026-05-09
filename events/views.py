from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, Participant

def events_list(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'events/list.html', {'events': events})

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = Participant.objects.filter(event=event, user=request.user).exists()
    return render(request, 'events/detail.html', {
        'event': event,
        'is_registered': is_registered,
    })

@login_required
def register_event(request, id):
    event = get_object_or_404(Event, id=id)
    
    if Participant.objects.filter(event=event, user=request.user).exists():
        messages.warning(request, "Vous êtes déjà inscrit à cet événement.")
        return redirect('event_detail', id=event.id)
    
    if event.is_full():
        messages.error(request, "Désolé, cet événement est complet.")
        return redirect('event_detail', id=event.id)
    
    Participant.objects.create(event=event, user=request.user)
    messages.success(request, f"✅ Vous êtes inscrit à {event.title} !")
    return redirect('dashboard')

# ========== VUES ADMINISTRATION ==========

@login_required
def add_event(request):
    """Ajouter un événement (admin uniquement)"""
    # Vérifier les droits - SEUL SUPERUSER
    if not request.user.is_superuser:
        messages.error(request, "⛔ Vous n'avez pas les droits pour ajouter un événement.")
        return redirect('events_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date_str = request.POST.get('date')
        location = request.POST.get('location')
        location_link = request.POST.get('location_link')
        image = request.FILES.get('image')
        max_participants = request.POST.get('max_participants', 0)
        status = request.POST.get('status', 'upcoming')
        is_featured = request.POST.get('is_featured') == 'on'
        
        # Validation
        if not title or not description or not date_str or not location:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'events/add_event.html')
        
        # Créer l'événement
        event = Event.objects.create(
            title=title,
            description=description,
            date=date_str,
            location=location,
            location_link=location_link,
            image=image,
            max_participants=int(max_participants) if max_participants else 0,
            status=status,
            is_featured=is_featured
        )
        
        messages.success(request, f'✨ Événement "{title}" créé avec succès !')
        return redirect('events_list')
    
    return render(request, 'events/add_event.html')

@login_required
def event_edit(request, id):
    """Modifier un événement (admin uniquement)"""
    # Vérifier les droits - SEUL SUPERUSER
    if not request.user.is_superuser:
        messages.error(request, "⛔ Vous n'avez pas les droits pour modifier un événement.")
        return redirect('events_list')
    
    event = get_object_or_404(Event, id=id)
    
    if request.method == 'POST':
        # Récupérer les données
        event.title = request.POST.get('title')
        event.description = request.POST.get('description')
        date_str = request.POST.get('date')
        if date_str:
            event.date = date_str
        event.location = request.POST.get('location')
        event.location_link = request.POST.get('location_link')
        
        if request.FILES.get('image'):
            event.image = request.FILES.get('image')
        
        event.max_participants = int(request.POST.get('max_participants', 0)) if request.POST.get('max_participants') else 0
        event.status = request.POST.get('status', 'upcoming')
        event.is_featured = request.POST.get('is_featured') == 'on'
        
        event.save()
        
        messages.success(request, f'✅ Événement "{event.title}" modifié avec succès !')
        return redirect('event_detail', id=event.id)
    
    return render(request, 'events/edit_event.html', {'event': event})

@login_required
def delete_event(request, id):
    """Supprimer un événement (admin uniquement)"""
    # Vérifier les droits - SEUL SUPERUSER
    if not request.user.is_superuser:
        messages.error(request, "⛔ Vous n'avez pas les droits pour supprimer un événement.")
        return redirect('events_list')
    
    event = get_object_or_404(Event, id=id)
    title = event.title
    event.delete()
    messages.success(request, f'✅ Événement "{title}" supprimé avec succès !')
    return redirect('events_list')

@login_required
def events_manage(request):
    """Page de gestion des événements (admin uniquement)"""
    # Vérifier les droits - SEUL SUPERUSER
    if not request.user.is_superuser:
        messages.error(request, "⛔ Accès réservé à l'administrateur!")
        return redirect('events_list')
    
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/manage.html', {'events': events})

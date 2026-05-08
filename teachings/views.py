from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Teaching
from .forms import TeachingForm

def teachings(request):
    """Afficher tous les enseignements"""
    teachings = Teaching.objects.all().order_by('-created_at')
    return render(request, 'teachings/teachings.html', {'teachings': teachings})

@staff_member_required
def add_teaching(request):
    """Ajouter un enseignement - formulaire personnalisé (admin uniquement)"""
    if request.method == 'POST':
        form = TeachingForm(request.POST, request.FILES)
        if form.is_valid():
            teaching = form.save()
            messages.success(request, f'✅ Enseignement "{teaching.title}" ajouté avec succès !')
            return redirect('teachings')
        else:
            messages.error(request, '❌ Erreur dans le formulaire. Vérifiez les champs.')
    else:
        form = TeachingForm()
    
    return render(request, 'teachings/add_teaching.html', {'form': form})

@staff_member_required
def delete_teaching(request, id):
    """Supprimer un enseignement (admin uniquement)"""
    teaching = get_object_or_404(Teaching, id=id)
    title = teaching.title
    teaching.delete()
    messages.success(request, f'✅ Enseignement "{title}" supprimé avec succès !')
    return redirect('teachings')
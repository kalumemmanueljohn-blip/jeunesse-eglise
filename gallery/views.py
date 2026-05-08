from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import GalleryImage, GalleryVideo, GalleryCategory
from .forms import GalleryImageForm, GalleryVideoForm
def gallery(request):
    images = GalleryImage.objects.all().order_by('-taken_at', '-uploaded_at')
    videos = GalleryVideo.objects.all().order_by('-uploaded_at')
    
    context = {
        'images': images,
        'videos': videos,
    }
    return render(request, 'gallery/gallery.html', context)

@staff_member_required
def add_photo(request):
    """Ajouter une photo - formulaire personnalisé"""
    if request.method == 'POST':
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Photo ajoutée avec succès !")
            return redirect('gallery')
        else:
            messages.error(request, "❌ Erreur dans le formulaire. Vérifiez les champs.")
    else:
        form = GalleryImageForm()
    
    return render(request, 'gallery/add_photo.html', {'form': form})

@staff_member_required
def add_video(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_url = request.POST.get('video_url')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        category_id = request.POST.get('category')
        
        # Au moins un des deux (lien ou fichier) doit être fourni
        if not video_url and not video_file:
            messages.error(request, "❌ Veuillez fournir un lien YouTube OU un fichier vidéo.")
            return redirect('add_video')
        
        category = None
        if category_id:
            from .models import GalleryCategory
            category = GalleryCategory.objects.get(id=category_id)
        
        video = GalleryVideo(
            title=title,
            description=description,
            video_url=video_url,
            video_file=video_file,
            thumbnail=thumbnail,
            category=category
        )
        video.save()
        messages.success(request, "✅ Vidéo ajoutée avec succès !")
        return redirect('gallery')
    
    from .models import GalleryCategory
    categories = GalleryCategory.objects.all()
    return render(request, 'gallery/add_video.html', {'categories': categories})

@staff_member_required
def delete_photo(request, id):
    """Supprimer une photo (admin uniquement)"""
    photo = get_object_or_404(GalleryImage, id=id)
    title = photo.title
    photo.delete()
    messages.success(request, f'✅ Photo "{title}" supprimée avec succès !')
    return redirect('gallery')

@staff_member_required
def delete_video(request, id):
    """Supprimer une vidéo (admin uniquement)"""
    video = get_object_or_404(GalleryVideo, id=id)
    title = video.title
    video.delete()
    messages.success(request, f'✅ Vidéo "{title}" supprimée avec succès !')
    return redirect('gallery')

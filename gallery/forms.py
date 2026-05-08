from django import forms
from .models import GalleryImage, GalleryVideo, GalleryCategory

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'description', 'image', 'category', 'taken_at', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Camp de jeunes 2024'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la photo...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'taken_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': '📌 Titre de la photo',
            'description': '📝 Description',
            'image': '🖼️ Image',
            'category': '📂 Catégorie',
            'taken_at': '📅 Date de l\'événement',
            'is_featured': '⭐ Mettre en avant',
        }

class GalleryVideoForm(forms.ModelForm):
    class Meta:
        model = GalleryVideo
        fields = ['title', 'description', 'video_url', 'thumbnail', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Concert de louange 2024'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la vidéo...'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': '📌 Titre de la vidéo',
            'description': '📝 Description',
            'video_url': '🔗 Lien YouTube/Vimeo',
            'thumbnail': '🖼️ Miniature (optionnel)',
            'category': '📂 Catégorie',
        }
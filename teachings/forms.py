from django import forms
from .models import Teaching

class TeachingForm(forms.ModelForm):
    class Meta:
        model = Teaching
        fields = ['title', 'speaker', 'description', 'content_type', 'file', 'video_url', 'duration', 'is_featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: La puissance de la prière'}),
            'speaker': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Pasteur Jean'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez le contenu de cet enseignement...'}),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 35min'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': '📌 Titre de l\'enseignement',
            'speaker': '🎤 Prédicateur / Enseignant',
            'description': '📖 Description',
            'content_type': '🎯 Type de contenu',
            'file': '📁 Fichier (MP3, MP4, PDF)',
            'video_url': '🔗 Lien YouTube / Vimeo (optionnel)',
            'duration': '⏱️ Durée',
            'is_featured': '⭐ Mettre en avant (À la une)',
        }
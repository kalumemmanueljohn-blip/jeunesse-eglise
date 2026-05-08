from django import forms
from .models import BlogPost

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'excerpt', 'content', 'featured_image', 'author', 'status', 'is_featured', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Comment j\'ai retrouvé la paix'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Résumé de l\'article...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Écrivez votre article ici...'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'foi, témoignage, prière (séparés par des virgules)'}),
        }
        labels = {
            'title': '📌 Titre de l\'article',
            'excerpt': '📝 Résumé (accroche)',
            'content': '✍️ Contenu de l\'article',
            'featured_image': '🖼️ Image à la une',
            'author': '👤 Auteur',
            'status': '📊 Statut',
            'is_featured': '⭐ Mettre en avant',
            'tags': '🏷️ Tags (séparés par des virgules)',
        }
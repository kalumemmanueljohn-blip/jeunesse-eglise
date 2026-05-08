from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    # Champs du profil
    phone_number = forms.CharField(max_length=20, required=False, label="Téléphone")
    address = forms.CharField(max_length=255, required=False, label="Adresse")
    birth_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    member_type = forms.ChoiceField(choices=UserProfile.MEMBER_TYPE_CHOICES, required=True, label="Je suis")
    department = forms.ChoiceField(choices=[('', '--------')] + list(UserProfile.DEPARTMENT_CHOICES), required=False, label="Département")
    is_regular_member = forms.BooleanField(required=False, label="Je prie déjà dans cette église")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes CSS
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Aide pour les champs
        self.fields['username'].help_text = "150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement."
        self.fields['password1'].help_text = "Votre mot de passe doit contenir au moins 8 caractères."
        self.fields['password2'].help_text = "Saisissez le même mot de passe que précédemment."
    
    def clean(self):
        cleaned_data = super().clean()
        member_type = cleaned_data.get('member_type')
        department = cleaned_data.get('department')
        
        if member_type == 'staff' and not department:
            self.add_error('department', "Veuillez sélectionner votre département")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=True)
        
        # Mettre à jour le profil
        profile = user.profile
        profile.phone_number = self.cleaned_data.get('phone_number', '')
        profile.address = self.cleaned_data.get('address', '')
        profile.birth_date = self.cleaned_data.get('birth_date')
        profile.member_type = self.cleaned_data.get('member_type')
        profile.department = self.cleaned_data.get('department')
        profile.is_regular_member = self.cleaned_data.get('is_regular_member', False)
        
        # Si membre du staff, définir is_staff = True
        if profile.member_type == 'staff':
            user.is_staff = True
            user.save()
        
        profile.save()
        return user
# create_admin.py
import os
import django
import sys

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeunesse_eglise.settings')

# Ajoute le chemin du projet si nécessaire
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

# Définir les variables globales
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@exemple.com'
ADMIN_PASSWORD = 'admin123'  # Changez ce mot de passe après la première connexion

def create_admin_user():
    """Crée un administrateur avec tous les droits"""
    
    print("="*60)
    print("🔧 CRÉATION DE L'ADMINISTRATEUR PRINCIPAL")
    print("="*60)
    
    # Vérifier si l'utilisateur existe déjà
    user = User.objects.filter(username=ADMIN_USERNAME).first()
    
    if user:
        print(f"⚠️ L'utilisateur '{ADMIN_USERNAME}' existe déjà.")
        print(f"   - is_staff: {user.is_staff}")
        print(f"   - is_superuser: {user.is_superuser}")
        print(f"   - is_active: {user.is_active}")
        
        # Mettre à jour les droits pour être sûr
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        print(f"✅ Droits administrateur complets attribués à '{ADMIN_USERNAME}'!")
        
    else:
        # Créer un nouveau superutilisateur
        user = User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
        
        # S'assurer que tous les droits sont activés
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        
        print(f"✅ Nouvel administrateur '{ADMIN_USERNAME}' créé avec succès!")
    
    # Afficher les informations de l'utilisateur
    print("\n" + "-"*40)
    print("📋 INFORMATIONS DE L'UTILISATEUR:")
    print(f"   - Nom d'utilisateur: {user.username}")
    print(f"   - Email: {user.email}")
    print(f"   - Staff: {user.is_staff}")
    print(f"   - Superuser: {user.is_superuser}")
    print(f"   - Actif: {user.is_active}")
    print("-"*40)
    
    # Vérifier et créer les groupes par défaut si nécessaire
    create_default_groups(user)
    
    return user

def create_default_groups(admin_user):
    """Crée les groupes par défaut et assigne l'admin comme super-admin"""
    
    print("\n👥 CONFIGURATION DES GROUPES ET PERMISSIONS:")
    
    # Liste des groupes à créer
    groups = {
        'Super Administrateurs': ['Tous les droits sur toutes les applications'],
        'Modérateurs': ['Gérer les utilisateurs', 'Modérer les commentaires', 'Gérer les événements'],
        'Éditeurs de contenu': ['Publier des articles', 'Gérer la galerie', 'Gérer les enseignements'],
        'Membres Staff': ['Accès au dashboard staff', 'Gérer les abonnés WhatsApp'],
    }
    
    for group_name, permissions_desc in groups.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"   ✅ Groupe '{group_name}' créé")
        else:
            print(f"   ⚠️ Groupe '{group_name}' existait déjà")
    
    # Assigner l'admin à tous les groupes (optionnel)
    admin_user.groups.clear()  # Nettoyer les groupes existants
    for group in Group.objects.all():
        admin_user.groups.add(group)
    
    # Assigner toutes les permissions
    if admin_user.is_superuser:
        print(f"\n👑 L'utilisateur '{admin_user.username}' a tous les droits superutilisateur!")
        print("   ✅ Accès complet à toutes les fonctionnalités d'administration")
    
    print("\n" + "="*60)
    print("🎉 ADMINISTRATEUR CONFIGURÉ AVEC SUCCÈS!")
    print(f"🔑 Identifiants de connexion:")
    print(f"   - Nom d'utilisateur: {admin_user.username}")
    print(f"   - Mot de passe: {ADMIN_PASSWORD}")
    print("="*60)
    print("\n⚠️ IMPORTANT: Changez ce mot de passe après la première connexion!")

def list_all_admins():
    """Affiche tous les administrateurs existants"""
    print("\n" + "="*60)
    print("📊 LISTE DES ADMINISTRATEURS EXISTANTS:")
    admins = User.objects.filter(is_superuser=True)
    
    if admins.exists():
        for admin in admins:
            print(f"   - {admin.username} (email: {admin.email})")
            print(f"     Staff: {admin.is_staff}, Superuser: {admin.is_superuser}, Actif: {admin.is_active}")
    else:
        print("   ⚠️ Aucun administrateur trouvé!")
    print("="*60)

if __name__ == '__main__':
    print("\n🚀 DÉBUT DE L'INSTALLATION DE L'ADMINISTRATEUR\n")
    
    # Créer l'administrateur principal
    admin_user = create_admin_user()
    
    # Lister tous les administrateurs existants
    list_all_admins()
    
    print("\n✨ Configuration terminée!")

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-this-in-production-123456789'

DEBUG = True

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# ============================================
# APPLICATIONS INSTALLÉES
# ============================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Applications du projet
    'core',
    'accounts',
    'events',
    'teachings',
    'blog',
    'donations',
    'gallery',
    'chat',  # ⚠️ AJOUTER L'APPLICATION CHAT
    
    # Pour WebSocket (optionnel mais recommandé)
    'channels',
]

ROOT_URLCONF = 'jeunesse_eglise.urls'   # ← LIGNE MANQUANTE

# ============================================
# CHANNELS / WEBSOCKET (pour messages temps réel)
# ============================================

# Définir l'application ASGI pour les WebSockets
ASGI_APPLICATION = 'jeunesse_eglise.asgi.application'

# Configuration des channel layers
# Pour développement: utilise InMemoryChannelLayer
# Pour production: utilise Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # Pour production, décommentez et configurez Redis:
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [('127.0.0.1', 6379)],
        # },
    },
}

# ============================================
# MIDDLEWARE
# ============================================

# Activer le fuseau horaire
USE_TZ = True

# Définir le fuseau horaire de Kinshasa (RDC)
TIME_ZONE = 'Africa/Kinshasa'

# Langue française
LANGUAGE_CODE = 'fr-fr'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# TEMPLATES - CONTEXT PROCESSORS
# ============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'chat.context_processors.unread_messages_count',
            ],
            # ⚠️ COMMENTE OU SUPPRIME LA PARTIE LIBRARIES
            # 'libraries': {
            #     'chat_extras': 'chat.templatetags.chat_extras',
            # },
        },
    },
]

# ============================================
# AUTHENTIFICATION
# ============================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# ============================================
# FICHIERS STATIQUES ET MÉDIAS
# ============================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/render/project/src/staticfiles'  # 👈 Ajoutez cette ligne


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================
# SÉCURITÉ POUR LES FICHIERS
# ============================================

# Augmenter la limite à 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Pour les très gros fichiers (100MB+)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # ← Vérifie que cette ligne existe
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuration pour l'upload de fichiers
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Augmenter la limite à 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB

# Pour les très gros fichiers (100MB+)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
# ============================================
# MESSAGERIE - CONFIGURATION DU CHAT
# ============================================

# Temps d'attente pour l'indicateur de saisie (en secondes)
CHAT_TYPING_TIMEOUT = 3

# Nombre maximum de fichiers par message
CHAT_MAX_FILES_PER_MESSAGE = 5

# Types de fichiers autorisés dans le chat
CHAT_ALLOWED_FILE_TYPES = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.webm'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
}

# Taille maximale par type de fichier (en bytes)
CHAT_MAX_FILE_SIZES = {
    'image': 5 * 1024 * 1024,    # 5 MB
    'video': 20 * 1024 * 1024,   # 20 MB
    'audio': 10 * 1024 * 1024,   # 10 MB
    'document': 10 * 1024 * 1024, # 10 MB
    'default': 10 * 1024 * 1024,  # 10 MB
}

# Nombre maximal de messages à charger par pagination
CHAT_MESSAGES_PER_PAGE = 50

# Nombre maximal de conversations à afficher
CHAT_MAX_CONVERSATIONS = 50

# ============================================
# SÉCURITÉ POUR LE CHAT
# ============================================

# Délai de modération automatique des messages
CHAT_AUTO_MODERATION_DELAY = 0  # 0 = désactivé, sinon en secondes

# Mots interdits (auto-modération)
CHAT_FILTERED_WORDS = [
    # Liste des mots à filtrer (optionnel)
]

# ============================================
# FICHIERS STATIQUES (pour production)
# ============================================

if not DEBUG:
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
    
    # Sécurité supplémentaire pour les médias
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
DEBUG = True  # ← Doit être True pour voir l'erreur détaillée

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SÉCURITÉ - UTILISATION DES VARIABLES D'ENVIRONNEMENT
# ============================================

# Pour Render, utilisez les variables d'environnement
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production-123456789')

# DEBUG doit être False en production sur Render
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.onrender.com',  # Tous les sous-domaines onrender.com
    'localhost', 
    '127.0.0.1',
    'jeunesse-eglise.onrender.com',  # Votre domaine spécifique
]

CSRF_TRUSTED_ORIGINS = [
    'https://jeunesse-eglise.onrender.com',
    'https://*.onrender.com',
]

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
    
    # Third-party apps (pour Render)
    'whitenoise.runserver_nostatic',  # Pour les fichiers statiques
    'channels',  # WebSocket
    
    # Applications du projet
    'core',
    'accounts',
    'events',
    'teachings',
    'blog',
    'donations',
    'gallery',
    'chat',
]

# ============================================
# MIDDLEWARE (AVEC WHITENOISE)
# ============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # IMPORTANT pour les fichiers statiques
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ============================================
# ROOT URLCONF
# ============================================

ROOT_URLCONF = 'jeunesse_eglise.urls'

# ============================================
# TEMPLATES
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
            ],
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
# DATABASE - Configuration pour Render
# ============================================

# Utilise PostgreSQL sur Render, SQLite en local
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# ============================================
# CHANNELS / WEBSOCKET
# ============================================

ASGI_APPLICATION = 'jeunesse_eglise.asgi.application'

# Configuration Redis (à ajouter sur Render)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
        # Pour production avec Redis (sur Render, ajoutez Redis)
        # 'BACKEND': 'channels_redis.core.RedisChannelLayer',
        # 'CONFIG': {
        #     "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        # },
    },
}

# ============================================
# FICHIERS STATIQUES ET MÉDIAS
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# INTERNATIONALISATION
# ============================================

USE_TZ = True
TIME_ZONE = 'Africa/Kinshasa'
LANGUAGE_CODE = 'fr-fr'
USE_I18N = True
USE_L10N = True

# ============================================
# UPLOAD DE FICHIERS
# ============================================

# Augmenter la limite à 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50 MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# ============================================
# MESSAGERIE - CONFIGURATION DU CHAT
# ============================================

CHAT_TYPING_TIMEOUT = 3
CHAT_MAX_FILES_PER_MESSAGE = 5

CHAT_ALLOWED_FILE_TYPES = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'],
    'video': ['.mp4', '.mov', '.avi', '.mkv', '.webm'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a', '.webm'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xls', '.xlsx', '.ppt', '.pptx'],
}

CHAT_MAX_FILE_SIZES = {
    'image': 5 * 1024 * 1024,    # 5 MB
    'video': 20 * 1024 * 1024,   # 20 MB
    'audio': 10 * 1024 * 1024,   # 10 MB
    'document': 10 * 1024 * 1024, # 10 MB
    'default': 10 * 1024 * 1024,
}

CHAT_MESSAGES_PER_PAGE = 50
CHAT_MAX_CONVERSATIONS = 50
CHAT_AUTO_MODERATION_DELAY = 0
CHAT_FILTERED_WORDS = []

# ============================================
# SÉCURITÉ POUR LA PRODUCTION
# ============================================

if not DEBUG:
    # Sécurité supplémentaire pour les médias
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================
# LOGGING (pour debug sur Render)
# ============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}

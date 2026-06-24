from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================
# SÉCURITÉ - UTILISATION DES VARIABLES D'ENVIRONNEMENT
# ============================================

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-this-in-production-123456789')
DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '.onrender.com',
    'localhost', 
    '127.0.0.1',
    'jeunesse-eglise.onrender.com',
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
    
    # Third-party apps
    'whitenoise.runserver_nostatic',
    'channels',
    'storages',  # ⭐ Pour Supabase Storage
    'imagekit',  # Pour le traitement d'images
    
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
# MIDDLEWARE
# ============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
# DATABASE
# ============================================

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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ============================================
# STOCKAGE DES FICHIERS - SUPABASE STORAGE
# ============================================

# Détection de l'environnement
IS_RENDER = 'RENDER' in os.environ

if IS_RENDER:
    # ⭐ SUPABASE STORAGE EN PRODUCTION
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY') or os.environ.get('SUPABASE_ANON_KEY')
    SUPABASE_BUCKET = os.environ.get('SUPABASE_BUCKET', 'media')
    
    if SUPABASE_URL and SUPABASE_KEY:
        print(f"☁️  Supabase Storage configuré: {SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/")
        
        # Configuration du stockage Supabase
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        
        # Configuration S3 compatible avec Supabase
        AWS_ACCESS_KEY_ID = os.environ.get('SUPABASE_ACCESS_KEY_ID', '')
        AWS_SECRET_ACCESS_KEY = os.environ.get('SUPABASE_SECRET_ACCESS_KEY', '')
        AWS_STORAGE_BUCKET_NAME = SUPABASE_BUCKET
        AWS_S3_ENDPOINT_URL = f"{SUPABASE_URL}/storage/v1/s3"
        AWS_S3_REGION_NAME = os.environ.get('SUPABASE_REGION', 'us-east-1')
        AWS_S3_USE_SSL = True
        AWS_S3_VERIFY = True
        AWS_QUERYSTRING_AUTH = False  # Désactiver l'authentification dans les URLs
        AWS_DEFAULT_ACL = 'public-read'
        
        # Personnalisation des URLs
        MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/"
        
        print(f"🌐 MEDIA_URL: {MEDIA_URL}")
    else:
        print("⚠️  Supabase Storage non configuré, utilisation du stockage local")
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # 📁 STOCKAGE LOCAL EN DÉVELOPPEMENT
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ============================================
# FICHIERS STATIQUES
# ============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'static']

if IS_RENDER:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
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
    'image': 5 * 1024 * 1024,
    'video': 20 * 1024 * 1024,
    'audio': 10 * 1024 * 1024,
    'document': 10 * 1024 * 1024,
    'default': 10 * 1024 * 1024,
}

CHAT_MESSAGES_PER_PAGE = 50
CHAT_MAX_CONVERSATIONS = 50
CHAT_AUTO_MODERATION_DELAY = 0
CHAT_FILTERED_WORDS = []

# ============================================
# SÉCURITÉ
# ============================================

if not DEBUG and IS_RENDER:
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ============================================
# LOGGING
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

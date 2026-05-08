# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jeunesse_eglise.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

User.objects.create_superuser('admin', 'admin@exemple.com', 'admin123')
print("Admin créé avec succès !")

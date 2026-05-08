from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group

class JeunesseEgliseAdminSite(AdminSite):
    site_header = "Jeunesse Église - Administration"
    site_title = "Admin Jeunesse Église"
    index_title = "📊 Tableau de bord"

    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        app_names = {
            'core': '🏠 Contenu du site',
            'events': '📅 Événements',
            'teachings': '🎧 Enseignements',
            'blog': '✍️ Blog',
            'gallery': '📸 Galerie',
            'donations': '💰 Dons',
            'accounts': '👥 Utilisateurs',
            'auth': '🔐 Authentification',
        }
        
        for app in app_list:
            if app['app_label'] in app_names:
                app['name'] = app_names[app['app_label']]
        
        return app_list

# Remplacer l'admin par défaut
admin_site = JeunesseEgliseAdminSite(name='myadmin')
admin.site = admin_site
admin.autodiscover()

# Enregistrer les modèles par défaut
admin_site.register(User)
admin_site.register(Group)
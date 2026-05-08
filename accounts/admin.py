from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from events.models import Participant
from donations.models import Donation

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'events_count', 'donations_count']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['last_login', 'date_joined', 'events_participated', 'user_donations']
    
    fieldsets = UserAdmin.fieldsets + (
        ('📅 Activité sur le site', {
            'fields': ('events_participated', 'user_donations'),
            'classes': ('collapse',)
        }),
    )
    
    def events_count(self, obj):
        count = Participant.objects.filter(user=obj).count()
        return format_html('<span style="color: #3498db;">📅 {}</span>', count)
    events_count.short_description = "Événements"
    
    def donations_count(self, obj):
        count = Donation.objects.filter(user=obj, status='confirmed').count()
        return format_html('<span style="color: #27ae60;">💰 {}</span>', count)
    donations_count.short_description = "Dons"
    
    def events_participated(self, obj):
        participants = Participant.objects.filter(user=obj).select_related('event')[:5]
        if not participants:
            return "Aucun événement"
        html = "<ul style='margin:0; padding-left:1rem;'>"
        for p in participants:
            html += f"<li>{p.event.title} - {p.registered_at.strftime('%d/%m/%Y')}</li>"
        html += "</ul>"
        if Participant.objects.filter(user=obj).count() > 5:
            html += "<p><small>...</small></p>"
        return format_html(html)
    events_participated.short_description = "Événements participés"
    
    def user_donations(self, obj):
        donations = Donation.objects.filter(user=obj, status='confirmed')[:5]
        if not donations:
            return "Aucun don"
        html = "<ul style='margin:0; padding-left:1rem;'>"
        for d in donations:
            html += f"<li>{d.amount}€ via {d.get_payment_method_display()} - {d.created_at.strftime('%d/%m/%Y')}</li>"
        html += "</ul>"
        if Donation.objects.filter(user=obj).count() > 5:
            html += "<p><small>...</small></p>"
        return format_html(html)
    user_donations.short_description = "Historique des dons"

# Réenregistrer User avec l'admin personnalisé
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
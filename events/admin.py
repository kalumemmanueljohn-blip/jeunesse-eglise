from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Event, Participant

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'status_badge', 'participants_count', 'is_featured', 'preview_image']
    list_filter = ['status', 'is_featured', 'date']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'participants_list']
    list_editable = ['is_featured']
    list_per_page = 20
    
    fieldsets = (
        ('📌 Informations principales', {
            'fields': ('title', 'description', 'image', 'status', 'is_featured')
        }),
        ('📅 Date et lieu', {
            'fields': ('date', 'location', 'location_link')
        }),
        ('👥 Participants', {
            'fields': ('max_participants', 'participants_list'),
            'classes': ('collapse',)
        }),
        ('📊 Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        if obj.status == 'upcoming':
            color = '#3498db'
            icon = '⏰'
            text = 'À venir'
        elif obj.status == 'ongoing':
            color = '#e74c3c'
            icon = '🔴'
            text = 'En cours'
        elif obj.status == 'past':
            color = '#95a5a6'
            icon = '✅'
            text = 'Passé'
        else:
            color = '#e74c3c'
            icon = '❌'
            text = 'Annulé'
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 15px; font-size: 11px;">{} {}</span>',
            color, icon, text
        )
    status_badge.short_description = "Statut"
    
    def participants_count(self, obj):
        count = obj.participants.count()
        if count > 0:
            return format_html('<span style="color: #27ae60; font-weight: bold;">👥 {}</span>', count)
        return format_html('<span style="color: #95a5a6;">👥 0</span>')
    participants_count.short_description = "Participants"
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 10px; object-fit: cover;" />',
                obj.image.url
            )
        return format_html('<span style="color: #95a5a6;">📷 Aucune</span>')
    preview_image.short_description = "Aperçu"
    
    def participants_list(self, obj):
        participants = obj.participants.select_related('user')[:10]
        if not participants:
            return "Aucun participant inscrit"
        
        html = '<table style="width: 100%; border-collapse: collapse;">'
        html += '<tr style="background: #f0f0f0;"><th style="padding: 5px;">Utilisateur</th><th style="padding: 5px;">Inscrit le</th><th style="padding: 5px;">Présent</th></tr>'
        for p in participants:
            html += f'''
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 5px;">{p.user.username}</td>
                    <td style="padding: 5px;">{p.registered_at.strftime('%d/%m/%Y %H:%M')}</td>
                    <td style="padding: 5px;">{"✅" if p.attended else "⏳"}</td>
                </tr>
            '''
        html += '</table>'
        
        if obj.participants.count() > 10:
            html += f'<p style="margin-top: 10px; color: #7f8c8d;">... et {obj.participants.count() - 10} autres participants</p>'
        
        return format_html(html)
    participants_list.short_description = "Liste des participants"
    
    actions = ['mark_as_featured', 'mark_as_upcoming', 'mark_as_ongoing', 'mark_as_past']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} événement(s) mis en avant.")
    mark_as_featured.short_description = "⭐ Mettre en avant"
    
    def mark_as_upcoming(self, request, queryset):
        queryset.update(status='upcoming')
        self.message_user(request, f"{queryset.count()} événement(s) marqué(s) comme À venir.")
    mark_as_upcoming.short_description = "⏰ Marquer comme À venir"
    
    def mark_as_ongoing(self, request, queryset):
        queryset.update(status='ongoing')
        self.message_user(request, f"{queryset.count()} événement(s) marqué(s) comme En cours.")
    mark_as_ongoing.short_description = "🔴 Marquer comme En cours"
    
    def mark_as_past(self, request, queryset):
        queryset.update(status='past')
        self.message_user(request, f"{queryset.count()} événement(s) marqué(s) comme Passé.")
    mark_as_past.short_description = "✅ Marquer comme Passé"

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at', 'attended']
    list_filter = ['attended', 'event', 'registered_at']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['registered_at']
    
    actions = ['mark_as_attended']
    
    def mark_as_attended(self, request, queryset):
        queryset.update(attended=True)
        self.message_user(request, f"{queryset.count()} participant(s) marqué(s) comme présent(s).")
    mark_as_attended.short_description = "✅ Marquer comme présent"
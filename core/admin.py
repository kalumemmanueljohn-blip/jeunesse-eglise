from django.contrib import admin
from .models import VerseOfTheDay, Testimonial
from django.contrib import admin
from .models import Subscriber

@admin.register(VerseOfTheDay)
class VerseOfTheDayAdmin(admin.ModelAdmin):
    list_display = ['reference', 'verse_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['verse', 'reference']
    
    def verse_preview(self, obj):
        return obj.verse[:50] + "..." if len(obj.verse) > 50 else obj.verse
    verse_preview.short_description = "Verset"

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'message_preview', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'message']
    
    def message_preview(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message
    message_preview.short_description = "Témoignage"
    
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'name', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['phone_number', 'name']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    
    actions = ['export_as_csv']
    
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="abonnes.csv"'
        writer = csv.writer(response)
        writer.writerow(['Numéro de téléphone', 'Nom', "Date d'inscription", 'Actif'])
        for obj in queryset:
            writer.writerow([
                obj.phone_number, 
                obj.name, 
                obj.created_at.strftime('%d/%m/%Y à %H:%M'), 
                'Oui' if obj.is_active else 'Non'
            ])
        return response
    export_as_csv.short_description = "📥 Exporter en CSV"
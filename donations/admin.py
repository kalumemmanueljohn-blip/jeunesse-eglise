from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method', 'anonymous', 'created_at']
    search_fields = ['user__username', 'transaction_id', 'phone_number']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def user_display(self, obj):
        if obj.anonymous:
            return "🔒 Anonyme"
        return obj.user.username if obj.user else "👤 Invité"
    user_display.short_description = "Donateur"
    
    actions = ['confirm_donations']
    
    def confirm_donations(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_donations.short_description = "✅ Confirmer les dons"
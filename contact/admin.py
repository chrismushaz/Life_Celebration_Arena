"""Admin configuration for contact and church info."""

from django.contrib import admin
from .models import ChurchInfo, ContactMessage


@admin.register(ChurchInfo)
class ChurchInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'pastor_name', 'phone', 'email']

    def has_add_permission(self, request):
        # Singleton: only allow one ChurchInfo record
        if ChurchInfo.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']

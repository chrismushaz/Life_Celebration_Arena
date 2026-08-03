"""Admin configuration for prayer requests."""

from django.contrib import admin
from .models import PrayerRequest


@admin.register(PrayerRequest)
class PrayerRequestAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'status', 'is_anonymous', 'is_public', 'created_at']
    list_filter = ['status', 'is_anonymous', 'is_public', 'created_at']
    search_fields = ['name', 'email', 'request_text']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

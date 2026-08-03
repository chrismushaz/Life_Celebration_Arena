"""Admin configuration for donations."""

from django.contrib import admin
from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor_name', 'amount', 'fund', 'frequency', 'status', 'created_at']
    list_filter = ['fund', 'frequency', 'status', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

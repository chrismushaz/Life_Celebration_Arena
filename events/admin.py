"""Admin configuration for events."""

from django.contrib import admin
from .models import Event, EventRegistration


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0
    readonly_fields = ['registered_at']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'location', 'is_featured', 'registration_required', 'is_active']
    list_filter = ['is_featured', 'registration_required', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    inlines = [EventRegistrationInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'event', 'guests', 'registered_at']
    list_filter = ['event', 'registered_at']
    search_fields = ['name', 'email']

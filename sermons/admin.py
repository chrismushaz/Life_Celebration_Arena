"""Admin configuration for sermons."""

from django.contrib import admin
from .models import Speaker, Sermon


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ['title', 'speaker', 'date_preached', 'series', 'is_featured', 'views_count']
    list_filter = ['speaker', 'date_preached', 'is_featured', 'series']
    search_fields = ['title', 'description', 'scripture_reference']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_preached'

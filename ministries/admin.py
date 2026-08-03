"""Admin configuration for ministries."""

from django.contrib import admin
from .models import Ministry, LeadershipMember


@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'ministry_type', 'is_active', 'order']
    list_filter = ['ministry_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LeadershipMember)
class LeadershipMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'title', 'is_active', 'order']
    list_filter = ['role', 'is_active']
    search_fields = ['name', 'bio']

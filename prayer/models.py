"""
Prayer request models with anonymous submission support.
"""

from django.conf import settings
from django.db import models


class PrayerRequest(models.Model):
    """Secure prayer request submitted by visitors."""

    STATUS_CHOICES = [
        ('new', 'New'),
        ('praying', 'Being Prayed For'),
        ('answered', 'Answered'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='prayer_requests',
    )
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    request_text = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False, help_text='Share on public prayer wall')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True, help_text='Internal notes (not visible to submitter)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        display_name = 'Anonymous' if self.is_anonymous else (self.name or 'Unknown')
        return f'Prayer Request from {display_name}'

    @property
    def display_name(self):
        if self.is_anonymous:
            return 'Anonymous'
        return self.name or 'Friend'

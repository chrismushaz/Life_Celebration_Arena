"""
Contact and church information models.
"""

from django.db import models


class ChurchInfo(models.Model):
    """
    Singleton-style church information for About page and site-wide context.
    Only one record should exist; managed via admin.
    """

    name = models.CharField(max_length=100, default='Grace Community Church')
    motto = models.CharField(max_length=200, default='Growing Together in Faith, Hope, and Love')
    tagline = models.CharField(max_length=200, blank=True)
    history = models.TextField(help_text='Church history')
    mission = models.TextField()
    vision = models.TextField()
    core_values = models.TextField(help_text='One value per line')
    pastor_name = models.CharField(max_length=100)
    pastor_title = models.CharField(max_length=100, default='Senior Pastor')
    pastor_message = models.TextField(help_text='Welcome message from the pastor')
    pastor_photo = models.ImageField(upload_to='church/', blank=True, null=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office_hours = models.TextField(help_text='Office hours, one line per day')
    google_maps_embed = models.TextField(blank=True, help_text='Google Maps iframe embed URL')
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    live_stream_url = models.URLField(blank=True, help_text='Live stream URL for Watch Live button')

    class Meta:
        verbose_name = 'Church Information'
        verbose_name_plural = 'Church Information'

    def __str__(self):
        return self.name

    @property
    def full_address(self):
        return f'{self.address}, {self.city}, {self.state} {self.zip_code}'


class ContactMessage(models.Model):
    """Contact form submission."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} - {self.name}'

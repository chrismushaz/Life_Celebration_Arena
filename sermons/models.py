"""
Sermon models for Grace Community Church.
Supports YouTube videos and downloadable audio.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Speaker(models.Model):
    """Sermon speaker / pastor."""

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, help_text='e.g. Senior Pastor')
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='speakers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Sermon(models.Model):
    """Sermon with video, audio, and metadata."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, related_name='sermons')
    scripture_reference = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    date_preached = models.DateField()
    youtube_url = models.URLField(blank=True, help_text='YouTube video URL')
    audio_file = models.FileField(upload_to='sermons/audio/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='sermons/thumbnails/', blank=True, null=True)
    series = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_preached']
        verbose_name = 'Sermon'
        verbose_name_plural = 'Sermons'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Sermon.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('sermons:detail', kwargs={'slug': self.slug})

    @property
    def youtube_embed_url(self):
        """Convert YouTube watch URL to embed URL."""
        if not self.youtube_url:
            return ''
        url = self.youtube_url
        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
        elif 'v=' in url:
            video_id = url.split('v=')[-1].split('&')[0]
        else:
            return url
        return f'https://www.youtube.com/embed/{video_id}'

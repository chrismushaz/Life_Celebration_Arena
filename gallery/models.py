"""
Gallery models for images and videos with categories.
"""

from django.db import models


class GalleryCategory(models.Model):
    """Gallery image/video category."""

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Gallery Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    """Gallery image with lightbox support."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/images/')
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='images',
    )
    is_featured = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class GalleryVideo(models.Model):
    """Gallery video (YouTube or uploaded)."""

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    youtube_url = models.URLField(blank=True)
    video_file = models.FileField(upload_to='gallery/videos/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/', blank=True, null=True)
    category = models.ForeignKey(
        GalleryCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='videos',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    @property
    def youtube_embed_url(self):
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

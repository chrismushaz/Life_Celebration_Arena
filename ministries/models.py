"""
Ministry and leadership team models.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Ministry(models.Model):
    """Church ministry (Children, Youth, Worship, etc.)."""

    MINISTRY_CHOICES = [
        ('children', "Children's Ministry"),
        ('youth', 'Youth Ministry'),
        ('women', "Women's Ministry"),
        ('men', "Men's Ministry"),
        ('worship', 'Worship Team'),
        ('evangelism', 'Evangelism Ministry'),
        ('outreach', 'Community Outreach'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    ministry_type = models.CharField(max_length=20, choices=MINISTRY_CHOICES, default='other')
    description = models.TextField()
    image = models.ImageField(upload_to='ministries/', blank=True, null=True)
    meeting_time = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Ministries'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ministries:detail', kwargs={'slug': self.slug})


class LeadershipMember(models.Model):
    """Church leadership team member."""

    ROLE_CHOICES = [
        ('pastor', 'Senior Pastor'),
        ('associate', 'Associate Pastor'),
        ('elder', 'Elder'),
        ('deacon', 'Deacon'),
        ('worship', 'Worship Leader'),
        ('youth', 'Youth Pastor'),
        ('admin', 'Administrator'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    title = models.CharField(max_length=100, blank=True)
    bio = models.TextField()
    photo = models.ImageField(upload_to='leadership/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.name} - {self.get_role_display()}'

"""Sitemap configuration for SEO."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import BlogPost
from events.models import Event
from ministries.models import Ministry
from sermons.models import Sermon


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['contact:home', 'contact:about', 'contact:contact',
                'sermons:list', 'ministries:list', 'events:list',
                'blog:list', 'gallery:gallery', 'prayer:submit', 'donations:give']

    def location(self, item):
        return reverse(item)


class SermonSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7

    def items(self):
        return Sermon.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return BlogPost.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.7

    def items(self):
        return Event.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.start_date


class MinistrySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6

    def items(self):
        return Ministry.objects.filter(is_active=True)

"""
Grace Community Church - Main URL configuration.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.generic import TemplateView

from .sitemaps import StaticViewSitemap, SermonSitemap, BlogSitemap, EventSitemap, MinistrySitemap

sitemaps = {
    'static': StaticViewSitemap,
    'sermons': SermonSitemap,
    'blog': BlogSitemap,
    'events': EventSitemap,
    'ministries': MinistrySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('contact.urls')),
    path('accounts/', include('accounts.urls')),
    path('sermons/', include('sermons.urls')),
    path('ministries/', include('ministries.urls')),
    path('events/', include('events.urls')),
    path('blog/', include('blog.urls')),
    path('gallery/', include('gallery.urls')),
    path('donations/', include('donations.urls')),
    path('prayer/', include('prayer.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
    ), name='robots'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

admin.site.site_header = 'Grace Community Church Admin'
admin.site.site_title = 'GCC Admin'
admin.site.index_title = 'Dashboard'

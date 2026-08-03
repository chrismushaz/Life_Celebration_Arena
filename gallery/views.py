"""Gallery views with category filtering."""

from django.views.generic import ListView

from .models import GalleryCategory, GalleryImage, GalleryVideo


def gallery_view(request):
    """Combined image and video gallery with category filter."""
    from django.shortcuts import render

    category_slug = request.GET.get('category')
    categories = GalleryCategory.objects.all()
    images = GalleryImage.objects.all()
    videos = GalleryVideo.objects.all()

    if category_slug:
        images = images.filter(category__slug=category_slug)
        videos = videos.filter(category__slug=category_slug)

    return render(request, 'gallery/gallery.html', {
        'images': images,
        'videos': videos,
        'categories': categories,
        'active_category': category_slug,
    })

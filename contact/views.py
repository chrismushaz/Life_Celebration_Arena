"""Home, About, and Contact views."""

from django.contrib import messages
from django.shortcuts import render

from blog.models import BlogPost
from events.models import Event
from ministries.models import LeadershipMember
from sermons.models import Sermon
from django.utils import timezone

from .forms import ContactForm
from .models import ChurchInfo, ContactMessage


def home_view(request):
    """Home page with hero, pastor message, and CTAs."""
    church = ChurchInfo.objects.first()
    featured_sermons = Sermon.objects.filter(is_featured=True)[:3]
    upcoming_events = Event.objects.filter(
        is_active=True, start_date__gte=timezone.now()
    )[:3]
    featured_event = Event.objects.filter(
        is_featured=True, is_active=True, start_date__gte=timezone.now()
    ).first()
    recent_posts = BlogPost.objects.filter(is_published=True)[:3]

    return render(request, 'contact/home.html', {
        'church': church,
        'featured_sermons': featured_sermons,
        'upcoming_events': upcoming_events,
        'featured_event': featured_event,
        'recent_posts': recent_posts,
    })


def about_view(request):
    """About Us page with history, mission, vision, values, and leadership."""
    church = ChurchInfo.objects.first()
    leadership = LeadershipMember.objects.filter(is_active=True)
    return render(request, 'contact/about.html', {
        'church': church,
        'leadership': leadership,
    })


def contact_view(request):
    """Contact page with form, map, and church details."""
    church = ChurchInfo.objects.first()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent. We will respond soon.')
            return render(request, 'contact/contact.html', {
                'form': ContactForm(),
                'church': church,
            })
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {
        'form': form,
        'church': church,
    })

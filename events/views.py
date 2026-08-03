"""Event list, detail, calendar, and registration views."""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView

from .forms import EventRegistrationForm
from .models import Event, EventRegistration


class EventListView(ListView):
    """Upcoming events list."""

    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(is_active=True, start_date__gte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_event'] = Event.objects.filter(
            is_featured=True, is_active=True, start_date__gte=timezone.now()
        ).first()
        context['past_events'] = Event.objects.filter(
            is_active=True, start_date__lt=timezone.now()
        )[:6]
        return context


class EventDetailView(DetailView):
    """Event detail with registration form."""

    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'
    slug_url_kwarg = 'slug'


def event_register(request, slug):
    """Handle event registration form submission."""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    if not event.registration_required:
        messages.warning(request, 'Registration is not required for this event.')
        return redirect('events:detail', slug=slug)

    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            if request.user.is_authenticated:
                registration.user = request.user
            registration.save()
            messages.success(request, f'Thank you! You are registered for {event.title}.')
            return redirect('events:detail', slug=slug)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': request.user.get_full_name(),
                'email': request.user.email,
                'phone': getattr(request.user, 'phone', ''),
            }
        form = EventRegistrationForm(initial=initial)

    return render(request, 'events/register.html', {'form': form, 'event': event})


def event_calendar(request):
    """Church calendar view."""
    events = Event.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'events/calendar.html', {'events': events})

"""Prayer request views."""

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PrayerRequestForm
from .models import PrayerRequest


def prayer_request_view(request):
    """Submit a prayer request with optional anonymous submission."""
    if request.method == 'POST':
        form = PrayerRequestForm(request.POST, user=request.user)
        if form.is_valid():
            prayer = form.save(commit=False)
            if request.user.is_authenticated:
                prayer.user = request.user
            if prayer.is_anonymous:
                prayer.name = ''
                prayer.email = ''
            prayer.save()
            messages.success(
                request,
                'Your prayer request has been submitted. Our prayer team is praying for you.',
            )
            return redirect('prayer:submit')
    else:
        form = PrayerRequestForm(user=request.user)

    public_requests = PrayerRequest.objects.filter(is_public=True, status__in=['new', 'praying'])[:10]
    return render(request, 'prayer/submit.html', {
        'form': form,
        'public_requests': public_requests,
    })

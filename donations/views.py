"""Donation and giving views."""

import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import DonationForm
from .models import Donation


def give_view(request):
    """Online giving page with multiple donation options."""
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            if request.user.is_authenticated:
                donation.user = request.user
            donation.status = 'completed'
            donation.transaction_id = f'GCC-{uuid.uuid4().hex[:12].upper()}'
            donation.save()
            messages.success(
                request,
                f'Thank you for your generous gift of ${donation.amount}! '
                f'Confirmation: {donation.transaction_id}',
            )
            return redirect('donations:give')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'donor_name': request.user.get_full_name(),
                'donor_email': request.user.email,
            }
        form = DonationForm(initial=initial)

    return render(request, 'donations/give.html', {'form': form})


@login_required
def donation_history(request):
    """Donation history for logged-in users."""
    donations = Donation.objects.filter(user=request.user)
    return render(request, 'donations/history.html', {'donations': donations})

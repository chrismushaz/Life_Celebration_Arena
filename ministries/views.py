"""Ministry and about views."""

from django.views.generic import ListView, DetailView

from .models import Ministry, LeadershipMember


class MinistryListView(ListView):
    """List all active ministries."""

    model = Ministry
    template_name = 'ministries/list.html'
    context_object_name = 'ministries'

    def get_queryset(self):
        return Ministry.objects.filter(is_active=True)


class MinistryDetailView(DetailView):
    """Ministry detail page."""

    model = Ministry
    template_name = 'ministries/detail.html'
    context_object_name = 'ministry'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Ministry.objects.filter(is_active=True)

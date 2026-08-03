"""Sermon list, detail, search, and filter views."""

from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import SermonSearchForm
from .models import Sermon


class SermonListView(ListView):
    """Display sermons with search and filter."""

    model = Sermon
    template_name = 'sermons/list.html'
    context_object_name = 'sermons'
    paginate_by = 9

    def get_queryset(self):
        queryset = Sermon.objects.select_related('speaker').all()
        form = SermonSearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            speaker = form.cleaned_data.get('speaker')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q)
                    | Q(description__icontains=q)
                    | Q(scripture_reference__icontains=q)
                    | Q(series__icontains=q)
                )
            if speaker:
                queryset = queryset.filter(speaker=speaker)
            if date_from:
                queryset = queryset.filter(date_preached__gte=date_from)
            if date_to:
                queryset = queryset.filter(date_preached__lte=date_to)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SermonSearchForm(self.request.GET)
        context['featured_sermons'] = Sermon.objects.filter(is_featured=True)[:3]
        return context


class SermonDetailView(DetailView):
    """Sermon detail with YouTube embed and audio download."""

    model = Sermon
    template_name = 'sermons/detail.html'
    context_object_name = 'sermon'
    slug_url_kwarg = 'slug'

    def get_object(self):
        obj = super().get_object()
        Sermon.objects.filter(pk=obj.pk).update(views_count=obj.views_count + 1)
        obj.refresh_from_db()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_sermons'] = (
            Sermon.objects.filter(speaker=self.object.speaker)
            .exclude(pk=self.object.pk)[:3]
        )
        return context

"""Sermon search and filter forms."""

from django import forms
from .models import Speaker


class SermonSearchForm(forms.Form):
    """Search and filter sermons by query, speaker, and date."""

    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search sermons...',
        }),
    )
    speaker = forms.ModelChoiceField(
        queryset=Speaker.objects.filter(is_active=True),
        required=False,
        empty_label='All Speakers',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

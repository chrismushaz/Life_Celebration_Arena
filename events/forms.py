"""Event registration form."""

from django import forms
from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    """Form for registering for church events."""

    class Meta:
        model = EventRegistration
        fields = ['name', 'email', 'phone', 'guests', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

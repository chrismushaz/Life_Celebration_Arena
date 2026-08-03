"""Prayer request form."""

from django import forms
from .models import PrayerRequest


class PrayerRequestForm(forms.ModelForm):
    """Secure prayer request form with anonymous option."""

    class Meta:
        model = PrayerRequest
        fields = ['name', 'email', 'request_text', 'is_anonymous', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email (optional)'}),
            'request_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your prayer request...',
            }),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['email'].required = False

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('is_anonymous') and not cleaned.get('name'):
            self.add_error('name', 'Please provide your name or check anonymous submission.')
        return cleaned

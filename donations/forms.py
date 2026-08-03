"""Donation form."""

from django import forms
from .models import Donation


class DonationForm(forms.ModelForm):
    """Online giving form with multiple fund options."""

    AMOUNT_CHOICES = [
        (25, '$25'),
        (50, '$50'),
        (100, '$100'),
        (250, '$250'),
        (500, '$500'),
        (0, 'Custom Amount'),
    ]

    preset_amount = forms.ChoiceField(
        choices=AMOUNT_CHOICES,
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Select Amount',
    )

    class Meta:
        model = Donation
        fields = ['donor_name', 'donor_email', 'amount', 'fund', 'frequency', 'is_anonymous', 'message']
        widgets = {
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'donor_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'step': '0.01'}),
            'fund': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount < 1:
            raise forms.ValidationError('Minimum donation amount is $1.')
        return amount

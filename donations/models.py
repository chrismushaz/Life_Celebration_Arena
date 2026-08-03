"""
Donation models for online giving.
"""

from django.conf import settings
from django.db import models


class Donation(models.Model):
    """Donation record for online giving."""

    FREQUENCY_CHOICES = [
        ('one_time', 'One Time'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    FUND_CHOICES = [
        ('general', 'General Fund'),
        ('missions', 'Missions'),
        ('building', 'Building Fund'),
        ('youth', 'Youth Ministry'),
        ('outreach', 'Community Outreach'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='donations',
    )
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fund = models.CharField(max_length=20, choices=FUND_CHOICES, default='general')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='one_time')
    is_anonymous = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'${self.amount} - {self.donor_name} ({self.get_fund_display()})'

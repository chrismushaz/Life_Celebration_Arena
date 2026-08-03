"""Donation URL configuration."""

from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.give_view, name='give'),
    path('history/', views.donation_history, name='history'),
]

"""Prayer URL configuration."""

from django.urls import path
from . import views

app_name = 'prayer'

urlpatterns = [
    path('', views.prayer_request_view, name='submit'),
]

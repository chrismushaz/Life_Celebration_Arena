"""Event URL configuration."""

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('calendar/', views.event_calendar, name='calendar'),
    path('<slug:slug>/', views.EventDetailView.as_view(), name='detail'),
    path('<slug:slug>/register/', views.event_register, name='register'),
]

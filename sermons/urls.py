"""Sermon URL configuration."""

from django.urls import path
from . import views

app_name = 'sermons'

urlpatterns = [
    path('', views.SermonListView.as_view(), name='list'),
    path('<slug:slug>/', views.SermonDetailView.as_view(), name='detail'),
]

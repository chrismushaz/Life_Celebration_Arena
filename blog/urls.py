"""Blog URL configuration."""

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='list'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
]

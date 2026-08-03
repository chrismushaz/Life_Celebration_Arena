"""Account views: registration, login, profile, password reset."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, CustomPasswordResetForm
from .models import User


class RegisterView(CreateView):
    """User registration with email field."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('contact:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            'Welcome to Grace Community Church! Your account has been created.',
        )
        return response


class UserLoginView(LoginView):
    """Custom login view with Bootstrap styling."""

    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    """Logout and redirect to home."""

    next_page = reverse_lazy('contact:home')


class UserPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/emails/password_reset_email.txt'
    subject_template_name = 'accounts/emails/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


@login_required
def profile_view(request):
    """Display user profile."""
    return render(request, 'accounts/profile.html', {'user': request.user})


class ProfileUpdateView(UpdateView):
    """Update user profile."""

    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated.')
        return super().form_valid(form)

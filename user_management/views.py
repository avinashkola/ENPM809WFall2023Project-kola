# user_management/views.py

import logging
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from .forms import ExtendedUserCreationForm
from django.http import HttpResponseServerError

logger = logging.getLogger(__name__)

class SignUp(CreateView):
    form_class = ExtendedUserCreationForm
    success_url = reverse_lazy('user_management:login')
    template_name = 'user_management/signup.html'

    def form_invalid(self, form):
        logger.error("Error in SignUp view. Form is invalid.")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    template_name = 'user_management/login.html'

    def form_invalid(self, form):
        logger.error("Error in CustomLoginView. Form is invalid.")
        return super().form_invalid(form)
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'user_management/password_reset.html'
    email_template_name = 'user_management/password_reset_email.html'
    success_url = reverse_lazy('user_management:password_reset_done')

    def form_invalid(self, form):
        logger.error("Error in CustomPasswordResetView. Form is invalid.")
        return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_management/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_management/password_reset_confirm.html'
    success_url = reverse_lazy('user_management:password_reset_complete')

    def form_invalid(self, form):
        logger.error("Error in CustomPasswordResetConfirmView. Form is invalid.")
        return super().form_invalid(form)

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_management/password_reset_complete.html'

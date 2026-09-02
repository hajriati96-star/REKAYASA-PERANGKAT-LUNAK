from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegistrasiUserForm, LoginForm


class RegistrasiView(CreateView):
    form_class = RegistrasiUserForm
    template_name = 'accounts/registrasi.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Akun berhasil dibuat. Silakan login.')
        return response


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Selamat datang, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

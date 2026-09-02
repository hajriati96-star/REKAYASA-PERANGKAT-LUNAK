from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Hanya user dengan role admin (atau superuser) yang boleh mengakses."""

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or getattr(user, 'is_admin_role', False))

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'Anda tidak memiliki izin untuk mengakses halaman ini.')
            return redirect('laporan:dashboard')
        return super().handle_no_permission()

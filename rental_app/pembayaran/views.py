from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Pembayaran
from .forms import PembayaranForm


class PembayaranListView(LoginRequiredMixin, ListView):
    model = Pembayaran
    template_name = 'pembayaran/pembayaran_list.html'
    context_object_name = 'daftar_pembayaran'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('penyewaan')


class PembayaranDetailView(LoginRequiredMixin, DetailView):
    model = Pembayaran
    template_name = 'pembayaran/pembayaran_detail.html'
    context_object_name = 'pembayaran'


class PembayaranCreateView(LoginRequiredMixin, CreateView):
    model = Pembayaran
    form_class = PembayaranForm
    template_name = 'pembayaran/pembayaran_form.html'
    success_url = reverse_lazy('pembayaran:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'Pembayaran sebesar Rp{form.instance.jumlah_pembayaran:,.0f} '.replace(',', '.') +
            f'untuk penyewaan #{form.instance.penyewaan.pk} berhasil dicatat.'
        )
        return response

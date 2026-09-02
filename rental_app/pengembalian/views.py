from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Pengembalian
from .forms import PengembalianForm


class PengembalianListView(LoginRequiredMixin, ListView):
    model = Pengembalian
    template_name = 'pengembalian/pengembalian_list.html'
    context_object_name = 'daftar_pengembalian'
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().select_related('penyewaan', 'penyewaan__alat')


class PengembalianDetailView(LoginRequiredMixin, DetailView):
    model = Pengembalian
    template_name = 'pengembalian/pengembalian_detail.html'
    context_object_name = 'pengembalian'


class PengembalianCreateView(LoginRequiredMixin, CreateView):
    model = Pengembalian
    form_class = PengembalianForm
    template_name = 'pengembalian/pengembalian_form.html'
    success_url = reverse_lazy('pengembalian:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        pesan = f'Pengembalian alat "{form.instance.penyewaan.alat.nama_alat}" berhasil dicatat.'
        if form.instance.keterlambatan > 0:
            pesan += (
                f' Terlambat {form.instance.keterlambatan} hari, '
                f'denda Rp{form.instance.denda_keterlambatan:,.0f}'.replace(',', '.')
            )
        messages.success(self.request, pesan)
        return response

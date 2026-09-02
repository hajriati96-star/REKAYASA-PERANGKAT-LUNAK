from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from .models import Penyewaan
from .forms import PenyewaanForm


class PenyewaanListView(LoginRequiredMixin, ListView):
    model = Penyewaan
    template_name = 'penyewaan/penyewaan_list.html'
    context_object_name = 'daftar_penyewaan'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('alat')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(nama_penyewa__icontains=q)
        return qs


class PenyewaanDetailView(LoginRequiredMixin, DetailView):
    model = Penyewaan
    template_name = 'penyewaan/penyewaan_detail.html'
    context_object_name = 'penyewaan'


class PenyewaanCreateView(LoginRequiredMixin, CreateView):
    model = Penyewaan
    form_class = PenyewaanForm
    template_name = 'penyewaan/penyewaan_form.html'
    success_url = reverse_lazy('penyewaan:list')

    def form_valid(self, form):
        form.instance.dibuat_oleh = self.request.user
        try:
            response = super().form_valid(form)
        except ValidationError as e:
            for field, msgs in getattr(e, 'message_dict', {'__all__': e.messages}).items():
                for msg in msgs:
                    form.add_error(field if field in form.fields else None, msg)
            return self.form_invalid(form)
        messages.success(
            self.request,
            f'Penyewaan untuk "{form.instance.alat.nama_alat}" oleh {form.instance.nama_penyewa} berhasil dibuat. '
            f'Total biaya: Rp{form.instance.total_biaya:,.0f}'.replace(',', '.')
        )
        return response

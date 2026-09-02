from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from accounts.mixins import AdminRequiredMixin
from .models import Alat
from .forms import AlatForm


class AlatListView(LoginRequiredMixin, ListView):
    model = Alat
    template_name = 'alat/alat_list.html'
    context_object_name = 'daftar_alat'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        if q:
            qs = qs.filter(nama_alat__icontains=q)
        if status:
            qs = qs.filter(status_alat=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = Alat.STATUS_CHOICES
        ctx['q'] = self.request.GET.get('q', '')
        ctx['status'] = self.request.GET.get('status', '')
        return ctx


class AlatDetailView(LoginRequiredMixin, DetailView):
    model = Alat
    template_name = 'alat/alat_detail.html'
    context_object_name = 'alat'


class AlatCreateView(AdminRequiredMixin, CreateView):
    model = Alat
    form_class = AlatForm
    template_name = 'alat/alat_form.html'
    success_url = reverse_lazy('alat:list')

    def form_valid(self, form):
        messages.success(self.request, f'Alat "{form.instance.nama_alat}" berhasil ditambahkan.')
        return super().form_valid(form)


class AlatUpdateView(AdminRequiredMixin, UpdateView):
    model = Alat
    form_class = AlatForm
    template_name = 'alat/alat_form.html'
    success_url = reverse_lazy('alat:list')

    def form_valid(self, form):
        messages.success(self.request, f'Data alat "{form.instance.nama_alat}" berhasil diperbarui.')
        return super().form_valid(form)


class AlatDeleteView(AdminRequiredMixin, DeleteView):
    model = Alat
    template_name = 'alat/alat_confirm_delete.html'
    success_url = reverse_lazy('alat:list')
    context_object_name = 'alat'

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            nama = self.object.nama_alat
            self.object.delete()
            messages.success(request, f'Alat "{nama}" berhasil dihapus.')
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(
                request,
                'Alat ini tidak dapat dihapus karena masih memiliki riwayat penyewaan terkait.'
            )
            return redirect('alat:detail', pk=kwargs['pk'])

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from alat.models import Alat
from pembayaran.models import Pembayaran
from pengembalian.models import Pengembalian
from penyewaan.models import Penyewaan


class DashboardView(LoginRequiredMixin, View):
    template_name = 'laporan/dashboard.html'

    def get(self, request):
        context = {
            'jumlah_alat_tersedia': Alat.objects.filter(status_alat=Alat.STATUS_TERSEDIA).count(),
            'jumlah_alat_disewa': Alat.objects.filter(status_alat=Alat.STATUS_DISEWA).count(),
            'jumlah_alat_rusak': Alat.objects.filter(status_alat=Alat.STATUS_RUSAK).count(),
            'jumlah_penyewaan_aktif': Penyewaan.objects.filter(pengembalian__isnull=True).count(),
            'pendapatan_bulan_ini': Pembayaran.objects.filter(
                status_pembayaran=Pembayaran.STATUS_LUNAS,
                tanggal_pembayaran__year=timezone.now().year,
                tanggal_pembayaran__month=timezone.now().month,
            ).aggregate(total=Sum('jumlah_pembayaran'))['total'] or Decimal('0'),
            'penyewaan_terbaru': Penyewaan.objects.select_related('alat').order_by('-dibuat_pada')[:5],
        }
        return render(request, self.template_name, context)


class LaporanAlatTersediaView(LoginRequiredMixin, View):
    template_name = 'laporan/alat_tersedia.html'

    def get(self, request):
        alat_list = Alat.objects.filter(status_alat=Alat.STATUS_TERSEDIA).order_by('nama_alat')
        return render(request, self.template_name, {'daftar_alat': alat_list})


class LaporanAlatDisewaView(LoginRequiredMixin, View):
    template_name = 'laporan/alat_disewa.html'

    def get(self, request):
        penyewaan_aktif = Penyewaan.objects.filter(
            pengembalian__isnull=True
        ).select_related('alat').order_by('tanggal_pengembalian_rencana')
        hari_ini = timezone.now().date()
        return render(request, self.template_name, {
            'daftar_penyewaan_aktif': penyewaan_aktif,
            'hari_ini': hari_ini,
        })


class LaporanPendapatanView(LoginRequiredMixin, View):
    template_name = 'laporan/pendapatan.html'

    def get(self, request):
        dari = request.GET.get('dari', '')
        sampai = request.GET.get('sampai', '')

        pembayaran_qs = Pembayaran.objects.filter(status_pembayaran=Pembayaran.STATUS_LUNAS)
        if dari:
            pembayaran_qs = pembayaran_qs.filter(tanggal_pembayaran__gte=dari)
        if sampai:
            pembayaran_qs = pembayaran_qs.filter(tanggal_pembayaran__lte=sampai)

        total = pembayaran_qs.aggregate(total=Sum('jumlah_pembayaran'))['total'] or Decimal('0')

        pendapatan_per_metode = (
            pembayaran_qs.values('metode_pembayaran')
            .annotate(total=Sum('jumlah_pembayaran'))
            .order_by('-total')
        )

        return render(request, self.template_name, {
            'total_pendapatan': total,
            'pendapatan_per_metode': pendapatan_per_metode,
            'daftar_pembayaran': pembayaran_qs.select_related('penyewaan').order_by('-tanggal_pembayaran'),
            'dari': dari,
            'sampai': sampai,
        })


class LaporanRiwayatPenyewaanView(LoginRequiredMixin, View):
    template_name = 'laporan/riwayat_penyewaan.html'

    def get(self, request):
        riwayat = Penyewaan.objects.select_related('alat').order_by('-dibuat_pada')
        return render(request, self.template_name, {'daftar_penyewaan': riwayat})


class LaporanPengembalianView(LoginRequiredMixin, View):
    template_name = 'laporan/pengembalian.html'

    def get(self, request):
        daftar = Pengembalian.objects.select_related(
            'penyewaan', 'penyewaan__alat'
        ).order_by('-dicatat_pada')
        return render(request, self.template_name, {'daftar_pengembalian': daftar})

from django.urls import path
from . import views

app_name = 'laporan'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('laporan/alat-tersedia/', views.LaporanAlatTersediaView.as_view(), name='alat_tersedia'),
    path('laporan/alat-disewa/', views.LaporanAlatDisewaView.as_view(), name='alat_disewa'),
    path('laporan/pendapatan/', views.LaporanPendapatanView.as_view(), name='pendapatan'),
    path('laporan/riwayat-penyewaan/', views.LaporanRiwayatPenyewaanView.as_view(), name='riwayat_penyewaan'),
    path('laporan/pengembalian/', views.LaporanPengembalianView.as_view(), name='pengembalian'),
]

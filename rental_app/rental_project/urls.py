from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('akun/', include('accounts.urls')),
    path('alat/', include('alat.urls')),
    path('penyewaan/', include('penyewaan.urls')),
    path('pengembalian/', include('pengembalian.urls')),
    path('pembayaran/', include('pembayaran.urls')),
    path('', include('laporan.urls')),
]

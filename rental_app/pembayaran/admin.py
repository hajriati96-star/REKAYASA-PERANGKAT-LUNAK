from django.contrib import admin
from .models import Pembayaran


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ['id', 'penyewaan', 'metode_pembayaran', 'jumlah_pembayaran', 'tanggal_pembayaran', 'status_pembayaran']
    list_filter = ['metode_pembayaran', 'status_pembayaran']

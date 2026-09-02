from django.contrib import admin
from .models import Pengembalian


@admin.register(Pengembalian)
class PengembalianAdmin(admin.ModelAdmin):
    list_display = ['id', 'penyewaan', 'tanggal_pengembalian', 'kondisi_alat', 'keterlambatan', 'denda_keterlambatan']
    list_filter = ['kondisi_alat']

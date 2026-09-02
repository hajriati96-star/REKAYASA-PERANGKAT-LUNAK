from django.contrib import admin
from .models import Penyewaan


@admin.register(Penyewaan)
class PenyewaanAdmin(admin.ModelAdmin):
    list_display = ['id', 'nama_penyewa', 'alat', 'tanggal_sewa', 'tanggal_pengembalian_rencana', 'total_biaya']
    search_fields = ['nama_penyewa']
    list_filter = ['tanggal_sewa']

from django.contrib import admin
from .models import Alat


@admin.register(Alat)
class AlatAdmin(admin.ModelAdmin):
    list_display = ['nama_alat', 'nomor_inventaris', 'jenis_alat', 'status_alat', 'harga_sewa_per_hari']
    list_filter = ['jenis_alat', 'status_alat']
    search_fields = ['nama_alat', 'nomor_inventaris']

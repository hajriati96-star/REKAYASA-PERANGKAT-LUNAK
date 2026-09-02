from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from alat.models import Alat
from penyewaan.models import Penyewaan


DENDA_PERSEN_PER_HARI = Decimal('0.10')  # 10% dari harga sewa harian, per hari keterlambatan


class Pengembalian(models.Model):
    KONDISI_BAIK = 'baik'
    KONDISI_RUSAK_RINGAN = 'rusak_ringan'
    KONDISI_RUSAK_BERAT = 'rusak_berat'
    KONDISI_HILANG = 'hilang'
    KONDISI_CHOICES = [
        (KONDISI_BAIK, 'Baik'),
        (KONDISI_RUSAK_RINGAN, 'Rusak Ringan'),
        (KONDISI_RUSAK_BERAT, 'Rusak Berat'),
        (KONDISI_HILANG, 'Hilang'),
    ]

    penyewaan = models.OneToOneField(
        Penyewaan, on_delete=models.PROTECT, related_name='pengembalian', verbose_name='Penyewaan terkait'
    )
    tanggal_pengembalian = models.DateField('Tanggal pengembalian')
    kondisi_alat = models.CharField('Kondisi alat', max_length=15, choices=KONDISI_CHOICES)
    keterlambatan = models.PositiveIntegerField('Keterlambatan (hari)', editable=False, default=0)
    denda_keterlambatan = models.DecimalField(
        'Denda keterlambatan (Rp)', max_digits=12, decimal_places=2, editable=False, default=Decimal('0')
    )
    catatan_kerusakan = models.TextField('Catatan kerusakan', blank=True)
    dicatat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pengembalian'
        verbose_name_plural = 'Data Pengembalian'
        ordering = ['-dicatat_pada']

    def __str__(self):
        return f'Pengembalian #{self.pk} - {self.penyewaan.nama_penyewa}'

    def clean(self):
        errors = {}

        if self.penyewaan_id and self.tanggal_pengembalian:
            if self.tanggal_pengembalian < self.penyewaan.tanggal_sewa:
                errors['tanggal_pengembalian'] = 'Tanggal pengembalian tidak boleh sebelum tanggal sewa.'
            elif self.tanggal_pengembalian > timezone.now().date():
                errors['tanggal_pengembalian'] = 'Tanggal pengembalian tidak boleh di masa depan.'

        if self.kondisi_alat in (self.KONDISI_RUSAK_RINGAN, self.KONDISI_RUSAK_BERAT, self.KONDISI_HILANG):
            if not self.catatan_kerusakan or not self.catatan_kerusakan.strip():
                errors['catatan_kerusakan'] = (
                    'Catatan kerusakan wajib diisi karena kondisi alat bukan "Baik".'
                )
            elif len(self.catatan_kerusakan.strip()) < 10:
                errors['catatan_kerusakan'] = 'Catatan kerusakan terlalu singkat, jelaskan minimal 10 karakter.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        rencana = self.penyewaan.tanggal_pengembalian_rencana
        selisih = (self.tanggal_pengembalian - rencana).days
        self.keterlambatan = max(0, selisih)
        harga_harian = self.penyewaan.alat.harga_sewa_per_hari
        self.denda_keterlambatan = (
            Decimal(self.keterlambatan) * harga_harian * DENDA_PERSEN_PER_HARI
        )

        super().save(*args, **kwargs)

        alat = self.penyewaan.alat
        if self.kondisi_alat == self.KONDISI_BAIK:
            alat.status_alat = Alat.STATUS_TERSEDIA
        elif self.kondisi_alat in (self.KONDISI_RUSAK_RINGAN, self.KONDISI_RUSAK_BERAT):
            alat.status_alat = Alat.STATUS_RUSAK
        else:
            alat.status_alat = Alat.STATUS_MAINTENANCE
        alat.save(update_fields=['status_alat'])

    @property
    def total_tagihan_akhir(self):
        return self.penyewaan.total_biaya + self.denda_keterlambatan

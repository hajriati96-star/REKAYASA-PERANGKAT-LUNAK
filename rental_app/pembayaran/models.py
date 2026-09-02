from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from penyewaan.models import Penyewaan


class Pembayaran(models.Model):
    METODE_TUNAI = 'tunai'
    METODE_TRANSFER = 'transfer'
    METODE_KARTU = 'kartu'
    METODE_EWALLET = 'ewallet'
    METODE_CHOICES = [
        (METODE_TUNAI, 'Tunai'),
        (METODE_TRANSFER, 'Transfer Bank'),
        (METODE_KARTU, 'Kartu Debit/Kredit'),
        (METODE_EWALLET, 'E-Wallet'),
    ]

    STATUS_PENDING = 'pending'
    STATUS_LUNAS = 'lunas'
    STATUS_GAGAL = 'gagal'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_LUNAS, 'Lunas'),
        (STATUS_GAGAL, 'Gagal'),
    ]

    penyewaan = models.ForeignKey(
        Penyewaan, on_delete=models.PROTECT, related_name='pembayaran_set', verbose_name='Penyewaan terkait'
    )
    metode_pembayaran = models.CharField('Metode pembayaran', max_length=10, choices=METODE_CHOICES)
    jumlah_pembayaran = models.DecimalField(
        'Jumlah pembayaran (Rp)', max_digits=12, decimal_places=2,
        validators=[MinValueValidator(1, 'Jumlah pembayaran harus lebih besar dari 0.')]
    )
    tanggal_pembayaran = models.DateField('Tanggal pembayaran')
    status_pembayaran = models.CharField(
        'Status pembayaran', max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    dicatat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pembayaran'
        verbose_name_plural = 'Data Pembayaran'
        ordering = ['-dicatat_pada']

    def __str__(self):
        return f'Pembayaran #{self.pk} - {self.penyewaan.nama_penyewa}'

    def clean(self):
        errors = {}

        if self.tanggal_pembayaran and self.penyewaan_id:
            if self.tanggal_pembayaran < self.penyewaan.tanggal_sewa:
                errors['tanggal_pembayaran'] = 'Tanggal pembayaran tidak boleh sebelum tanggal sewa.'
            elif self.tanggal_pembayaran > timezone.now().date():
                errors['tanggal_pembayaran'] = 'Tanggal pembayaran tidak boleh di masa depan.'

        if self.jumlah_pembayaran is not None and self.penyewaan_id and self.status_pembayaran == self.STATUS_LUNAS:
            sudah_dibayar = self.penyewaan.pembayaran_set.filter(
                status_pembayaran=self.STATUS_LUNAS
            ).exclude(pk=self.pk).aggregate(models.Sum('jumlah_pembayaran'))['jumlah_pembayaran__sum'] or Decimal('0')

            total_setelah = sudah_dibayar + self.jumlah_pembayaran
            if total_setelah > self.penyewaan.total_biaya:
                sisa = self.penyewaan.total_biaya - sudah_dibayar
                errors['jumlah_pembayaran'] = (
                    f'Jumlah pembayaran melebihi sisa tagihan. Sisa tagihan penyewaan ini '
                    f'adalah Rp{sisa:,.0f}.'.replace(',', '.')
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from accounts.models import phone_validator
from alat.models import Alat


nama_penyewa_validator = RegexValidator(
    regex=r"^[A-Za-z\s.'\-]+$",
    message="Nama penyewa hanya boleh berisi huruf, spasi, titik, apostrof, dan tanda hubung."
)


class Penyewaan(models.Model):
    nama_penyewa = models.CharField('Nama penyewa', max_length=100, validators=[nama_penyewa_validator])
    no_telepon_penyewa = models.CharField('Nomor telepon penyewa', max_length=15, validators=[phone_validator])
    alat = models.ForeignKey(
        Alat, on_delete=models.PROTECT, related_name='penyewaan_set', verbose_name='Alat yang disewa'
    )
    tanggal_sewa = models.DateField('Tanggal sewa')
    tanggal_pengembalian_rencana = models.DateField('Tanggal pengembalian (rencana)')
    lama_penyewaan = models.PositiveIntegerField('Lama penyewaan (hari)', editable=False, default=0)
    total_biaya = models.DecimalField(
        'Total biaya (Rp)', max_digits=12, decimal_places=2, editable=False, default=Decimal('0')
    )
    dibuat_oleh = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='penyewaan_dibuat'
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Penyewaan'
        verbose_name_plural = 'Data Penyewaan'
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f'Penyewaan #{self.pk} - {self.nama_penyewa} ({self.alat.nama_alat})'

    def clean(self):
        errors = {}

        if self.nama_penyewa:
            self.nama_penyewa = self.nama_penyewa.strip()
            if len(self.nama_penyewa) < 3:
                errors['nama_penyewa'] = 'Nama penyewa minimal 3 karakter.'

        if self.tanggal_sewa and self.tanggal_pengembalian_rencana:
            if self.tanggal_pengembalian_rencana <= self.tanggal_sewa:
                errors['tanggal_pengembalian_rencana'] = (
                    'Tanggal pengembalian rencana harus setelah tanggal sewa.'
                )
            lama = (self.tanggal_pengembalian_rencana - self.tanggal_sewa).days
            if lama > 90:
                errors['tanggal_pengembalian_rencana'] = (
                    'Durasi penyewaan tidak boleh lebih dari 90 hari. '
                    'Hubungi admin untuk penyewaan jangka panjang khusus.'
                )

        if self.tanggal_sewa and not self.pk:
            if self.tanggal_sewa < timezone.now().date():
                errors['tanggal_sewa'] = 'Tanggal sewa tidak boleh di masa lalu.'

        if self.alat_id and not self.pk:
            # Hanya divalidasi saat membuat penyewaan baru
            if self.alat.status_alat != Alat.STATUS_TERSEDIA:
                errors['alat'] = (
                    f'Alat "{self.alat.nama_alat}" berstatus '
                    f'"{self.alat.get_status_alat_display()}" dan tidak dapat disewa saat ini.'
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        is_baru = self._state.adding
        self.full_clean()

        if self.tanggal_sewa and self.tanggal_pengembalian_rencana:
            self.lama_penyewaan = (self.tanggal_pengembalian_rencana - self.tanggal_sewa).days
            self.total_biaya = Decimal(self.lama_penyewaan) * self.alat.harga_sewa_per_hari

        super().save(*args, **kwargs)

        if is_baru:
            self.alat.status_alat = Alat.STATUS_DISEWA
            self.alat.save(update_fields=['status_alat'])

    @property
    def sudah_dibayar(self):
        from pembayaran.models import Pembayaran
        total = self.pembayaran_set.filter(
            status_pembayaran=Pembayaran.STATUS_LUNAS
        ).aggregate(models.Sum('jumlah_pembayaran'))['jumlah_pembayaran__sum']
        return total or Decimal('0')

    @property
    def sisa_tagihan(self):
        return self.total_biaya - self.sudah_dibayar

    @property
    def sudah_dikembalikan(self):
        return hasattr(self, 'pengembalian')

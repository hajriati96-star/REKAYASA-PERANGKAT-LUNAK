from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.utils import timezone


nomor_inventaris_validator = RegexValidator(
    regex=r'^[A-Z]{2,5}-\d{3,6}$',
    message='Format nomor inventaris tidak valid. Contoh yang benar: KM-0001, DR-00023.'
)

warna_validator = RegexValidator(
    regex=r'^[A-Za-z\s]+$',
    message='Warna hanya boleh berisi huruf dan spasi, contoh: Hitam, Silver, Abu-abu Tua.'
)


class Alat(models.Model):
    JENIS_KAMERA = 'kamera'
    JENIS_LENSA = 'lensa'
    JENIS_LIGHTING = 'lighting'
    JENIS_AUDIO = 'audio'
    JENIS_TRIPOD = 'tripod'
    JENIS_DRONE = 'drone'
    JENIS_LAINNYA = 'lainnya'
    JENIS_CHOICES = [
        (JENIS_KAMERA, 'Kamera'),
        (JENIS_LENSA, 'Lensa'),
        (JENIS_LIGHTING, 'Lighting'),
        (JENIS_AUDIO, 'Audio'),
        (JENIS_TRIPOD, 'Tripod / Stabilizer'),
        (JENIS_DRONE, 'Drone'),
        (JENIS_LAINNYA, 'Lainnya'),
    ]

    STATUS_TERSEDIA = 'tersedia'
    STATUS_DISEWA = 'disewa'
    STATUS_RUSAK = 'rusak'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_CHOICES = [
        (STATUS_TERSEDIA, 'Tersedia'),
        (STATUS_DISEWA, 'Disewa'),
        (STATUS_RUSAK, 'Rusak'),
        (STATUS_MAINTENANCE, 'Dalam Perbaikan'),
    ]

    nama_alat = models.CharField('Nama alat', max_length=100)
    jenis_alat = models.CharField('Jenis alat', max_length=20, choices=JENIS_CHOICES)
    nomor_inventaris = models.CharField(
        'Nomor inventaris', max_length=30, unique=True, validators=[nomor_inventaris_validator]
    )
    tahun_pembelian = models.PositiveIntegerField('Tahun pembelian')
    warna = models.CharField('Warna', max_length=30, validators=[warna_validator])
    harga_sewa_per_hari = models.DecimalField(
        'Harga sewa per hari (Rp)', max_digits=12, decimal_places=2,
        validators=[MinValueValidator(1000, 'Harga sewa minimal Rp1.000 per hari.')]
    )
    status_alat = models.CharField(
        'Status alat', max_length=15, choices=STATUS_CHOICES, default=STATUS_TERSEDIA
    )
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alat'
        verbose_name_plural = 'Data Alat'
        ordering = ['nama_alat']

    def __str__(self):
        return f'{self.nama_alat} ({self.nomor_inventaris})'

    def clean(self):
        errors = {}
        current_year = timezone.now().year

        if self.tahun_pembelian is not None:
            if self.tahun_pembelian < 1990:
                errors['tahun_pembelian'] = 'Tahun pembelian tidak boleh sebelum tahun 1990.'
            elif self.tahun_pembelian > current_year:
                errors['tahun_pembelian'] = f'Tahun pembelian tidak boleh melebihi tahun {current_year}.'

        if self.nomor_inventaris:
            self.nomor_inventaris = self.nomor_inventaris.strip().upper()

        if self.nama_alat:
            self.nama_alat = self.nama_alat.strip()
            if len(self.nama_alat) < 3:
                errors['nama_alat'] = 'Nama alat minimal 3 karakter.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

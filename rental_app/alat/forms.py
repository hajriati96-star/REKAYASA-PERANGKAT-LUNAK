from django import forms

from .models import Alat

TEXT_INPUT_CLASS = 'form-control'


class AlatForm(forms.ModelForm):
    class Meta:
        model = Alat
        fields = [
            'nama_alat', 'jenis_alat', 'nomor_inventaris', 'tahun_pembelian',
            'warna', 'harga_sewa_per_hari', 'status_alat',
        ]
        widgets = {
            'nama_alat': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': 'Contoh: Kamera Sony A7 III'}),
            'jenis_alat': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
            'nomor_inventaris': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': 'Contoh: KM-0001'}),
            'tahun_pembelian': forms.NumberInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': '2023'}),
            'warna': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': 'Contoh: Hitam'}),
            'harga_sewa_per_hari': forms.NumberInput(attrs={'class': TEXT_INPUT_CLASS, 'step': '500', 'placeholder': '50000'}),
            'status_alat': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
        }

    def clean_nomor_inventaris(self):
        nomor = self.cleaned_data['nomor_inventaris'].strip().upper()
        qs = Alat.objects.filter(nomor_inventaris=nomor)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('Nomor inventaris ini sudah digunakan alat lain.')
        return nomor

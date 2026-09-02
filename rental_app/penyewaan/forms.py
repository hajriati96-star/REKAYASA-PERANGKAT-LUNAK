from django import forms

from alat.models import Alat
from .models import Penyewaan

TEXT_INPUT_CLASS = 'form-control'


class PenyewaanForm(forms.ModelForm):
    class Meta:
        model = Penyewaan
        fields = ['nama_penyewa', 'no_telepon_penyewa', 'alat', 'tanggal_sewa', 'tanggal_pengembalian_rencana']
        widgets = {
            'nama_penyewa': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': 'Nama lengkap penyewa'}),
            'no_telepon_penyewa': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': '081234567890'}),
            'alat': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
            'tanggal_sewa': forms.DateInput(attrs={'class': TEXT_INPUT_CLASS, 'type': 'date'}),
            'tanggal_pengembalian_rencana': forms.DateInput(attrs={'class': TEXT_INPUT_CLASS, 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Saat membuat baru, hanya tampilkan alat yang berstatus tersedia
        if not self.instance.pk:
            self.fields['alat'].queryset = Alat.objects.filter(status_alat=Alat.STATUS_TERSEDIA)
        if self.fields['alat'].queryset.count() == 0 and not self.instance.pk:
            self.fields['alat'].help_text = 'Tidak ada alat yang tersedia untuk disewa saat ini.'

    def clean(self):
        cleaned_data = super().clean()
        tanggal_sewa = cleaned_data.get('tanggal_sewa')
        tanggal_kembali = cleaned_data.get('tanggal_pengembalian_rencana')
        if tanggal_sewa and tanggal_kembali and tanggal_kembali <= tanggal_sewa:
            self.add_error(
                'tanggal_pengembalian_rencana',
                'Tanggal pengembalian rencana harus setelah tanggal sewa.'
            )
        return cleaned_data

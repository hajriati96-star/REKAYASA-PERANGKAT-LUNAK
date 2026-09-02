from django import forms

from penyewaan.models import Penyewaan
from .models import Pembayaran

TEXT_INPUT_CLASS = 'form-control'


class PembayaranForm(forms.ModelForm):
    penyewaan = forms.ModelChoiceField(
        queryset=Penyewaan.objects.none(),
        widget=forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
        label='Penyewaan'
    )

    class Meta:
        model = Pembayaran
        fields = ['penyewaan', 'metode_pembayaran', 'jumlah_pembayaran', 'tanggal_pembayaran', 'status_pembayaran']
        widgets = {
            'metode_pembayaran': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
            'jumlah_pembayaran': forms.NumberInput(attrs={'class': TEXT_INPUT_CLASS, 'step': '500'}),
            'tanggal_pembayaran': forms.DateInput(attrs={'class': TEXT_INPUT_CLASS, 'type': 'date'}),
            'status_pembayaran': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['penyewaan'].queryset = Penyewaan.objects.select_related('alat').order_by('-dibuat_pada')

    def clean_jumlah_pembayaran(self):
        jumlah = self.cleaned_data['jumlah_pembayaran']
        if jumlah <= 0:
            raise forms.ValidationError('Jumlah pembayaran harus lebih besar dari 0.')
        return jumlah

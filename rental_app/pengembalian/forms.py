from django import forms

from penyewaan.models import Penyewaan
from .models import Pengembalian

TEXT_INPUT_CLASS = 'form-control'


class PengembalianForm(forms.ModelForm):
    penyewaan = forms.ModelChoiceField(
        queryset=Penyewaan.objects.none(),
        widget=forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
        label='Penyewaan'
    )

    class Meta:
        model = Pengembalian
        fields = ['penyewaan', 'tanggal_pengembalian', 'kondisi_alat', 'catatan_kerusakan']
        widgets = {
            'tanggal_pengembalian': forms.DateInput(attrs={'class': TEXT_INPUT_CLASS, 'type': 'date'}),
            'kondisi_alat': forms.Select(attrs={'class': TEXT_INPUT_CLASS}),
            'catatan_kerusakan': forms.Textarea(
                attrs={'class': TEXT_INPUT_CLASS, 'rows': 3, 'placeholder': 'Wajib diisi jika kondisi tidak baik'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hanya penyewaan yang belum ada catatan pengembaliannya
        self.fields['penyewaan'].queryset = Penyewaan.objects.filter(
            pengembalian__isnull=True
        ).select_related('alat')

    def clean(self):
        cleaned_data = super().clean()
        kondisi = cleaned_data.get('kondisi_alat')
        catatan = cleaned_data.get('catatan_kerusakan', '')
        if kondisi and kondisi != Pengembalian.KONDISI_BAIK:
            if not catatan or len(catatan.strip()) < 10:
                self.add_error(
                    'catatan_kerusakan',
                    'Catatan kerusakan wajib diisi (minimal 10 karakter) jika kondisi alat tidak baik.'
                )
        return cleaned_data

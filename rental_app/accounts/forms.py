from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from .models import User


TEXT_INPUT_CLASS = 'form-control'


class RegistrasiUserForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': 'nama@contoh.com'})
    )
    phone_number = forms.CharField(
        label='Nomor telepon', required=True,
        widget=forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'placeholder': '081234567890'})
    )
    address = forms.CharField(
        label='Alamat', required=True,
        widget=forms.Textarea(attrs={'class': TEXT_INPUT_CLASS, 'rows': 3})
    )
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': TEXT_INPUT_CLASS}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': TEXT_INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': TEXT_INPUT_CLASS})
        self.fields['password2'].widget.attrs.update({'class': TEXT_INPUT_CLASS})

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if len(username) < 4:
            raise ValidationError('Nama pengguna minimal 4 karakter.')
        if not username.replace('_', '').isalnum():
            raise ValidationError('Nama pengguna hanya boleh berisi huruf, angka, dan underscore.')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('Nama pengguna ini sudah digunakan.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email ini sudah terdaftar.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if User.objects.filter(phone_number=phone).exists():
            raise ValidationError('Nomor telepon ini sudah terdaftar.')
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address', '').strip()
        if len(address) < 10:
            raise ValidationError('Alamat terlalu singkat, minimal 10 karakter.')
        return address


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': TEXT_INPUT_CLASS, 'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': TEXT_INPUT_CLASS}))

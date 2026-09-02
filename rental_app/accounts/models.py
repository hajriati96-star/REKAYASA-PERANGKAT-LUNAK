from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r'^(\+62|62|0)8[1-9][0-9]{6,10}$',
    message='Nomor telepon harus format Indonesia yang valid, contoh: 081234567890 atau +6281234567890.'
)


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_PETUGAS = 'petugas'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_PETUGAS, 'Petugas'),
    ]

    email = models.EmailField('Alamat email', unique=True)
    phone_number = models.CharField(
        'Nomor telepon', max_length=15, unique=True, validators=[phone_validator]
    )
    address = models.TextField(
        'Alamat', validators=[MinLengthValidator(10, 'Alamat minimal 10 karakter.')]
    )
    role = models.CharField(
        'Role pengguna', max_length=10, choices=ROLE_CHOICES, default=ROLE_PETUGAS
    )

    REQUIRED_FIELDS = ['email', 'phone_number', 'address']

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_admin_role(self):
        return self.role == self.ROLE_ADMIN

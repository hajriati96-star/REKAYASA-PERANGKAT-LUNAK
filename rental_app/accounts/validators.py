import re
from django.core.exceptions import ValidationError


class ComplexPasswordValidator:
    """
    Mewajibkan password mengandung:
    - minimal 1 huruf besar
    - minimal 1 huruf kecil
    - minimal 1 angka
    - minimal 1 karakter simbol
    """

    def validate(self, password, user=None):
        errors = []
        if not re.search(r'[A-Z]', password):
            errors.append('Password harus mengandung minimal 1 huruf besar.')
        if not re.search(r'[a-z]', password):
            errors.append('Password harus mengandung minimal 1 huruf kecil.')
        if not re.search(r'[0-9]', password):
            errors.append('Password harus mengandung minimal 1 angka.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>_\-+=/\\\[\];\'~`]', password):
            errors.append('Password harus mengandung minimal 1 karakter simbol (!@#$%, dll).')
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return (
            'Password harus terdiri dari minimal 8 karakter dan mengandung '
            'kombinasi huruf besar, huruf kecil, angka, dan simbol.'
        )

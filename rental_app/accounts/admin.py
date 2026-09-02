from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'phone_number', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informasi Tambahan', {'fields': ('phone_number', 'address', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informasi Tambahan', {'fields': ('email', 'phone_number', 'address', 'role')}),
    )


admin.site.register(User, CustomUserAdmin)

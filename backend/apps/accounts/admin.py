from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'email', 'username', 'first_name', 'last_name', 'is_staff',
        'is_verified', 'notification_phone', 'cpf'
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'notification_phone',
                'photo',
                'cpf',
                'notify_chat',
                'notify_pet_found',
                'notify_other',
                'is_verified',
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'notification_phone',
                'photo',
                'cpf',
                'notify_chat',
                'notify_pet_found',
                'notify_other',
                'is_verified',
            )
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

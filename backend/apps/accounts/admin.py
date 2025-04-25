from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_staff', 'is_active', 'is_verified')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_verified')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'cpf', 'photo', 'notification_phone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
        ('Notificações', {'fields': ('notify_chat', 'notify_pet_found', 'notify_other')}),
        ('Verificação', {'fields': ('is_verified',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'is_staff', 'is_active', 'is_superuser',
                'notification_phone', 'cpf', 'photo',
                'notify_chat', 'notify_pet_found', 'notify_other', 'is_verified'
            )
        }),
    )

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from cloudinary.models import CloudinaryField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    notification_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Telefone para notificação"
    )
    photo = CloudinaryField(
        resource_type='image',
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        blank=True,
        null=True,
        help_text="CPF no formato XXX.XXX.XXX-XX"
    )
    notify_chat = models.BooleanField(default=True, help_text="Receber notificações de chat")
    notify_pet_found = models.BooleanField(default=True, help_text="Receber notificações de pet encontrado")
    notify_other = models.BooleanField(default=True, help_text="Receber outras notificações")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

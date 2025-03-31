from django.db import models  # Adicione esta linha
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('chat', 'Nova Mensagem de Chat'),
        ('pet_found', 'Pet Encontrado'),
        ('other', 'Outro'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='other')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} para {self.user.email}: {self.message}"
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('chat', 'Nova Mensagem de Chat'),
        ('pet_found', 'Pet Encontrado'),
        ('other', 'Outro'),
    )

    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='other')
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} para {self.user.email}: {self.message[:30]}"


class ChatMessage(models.Model):
    sender = models.ForeignKey('accounts.CustomUser', related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey('accounts.CustomUser', related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.message[:30]}"


class BlockedUser(models.Model):
    blocker = models.ForeignKey('accounts.CustomUser', related_name='blocked_users', on_delete=models.CASCADE)
    blocked = models.ForeignKey('accounts.CustomUser', related_name='blocked_by', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} bloqueou {self.blocked}"


class ChatReport(models.Model):
    reporter = models.ForeignKey('accounts.CustomUser', related_name='reports_made', on_delete=models.CASCADE)
    reported = models.ForeignKey('accounts.CustomUser', related_name='reports_received', on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, related_name='reports', on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Denúncia de {self.reporter} contra {self.reported}"

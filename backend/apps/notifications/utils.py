# apps/notifications/utils.py

from apps.notifications.models import Notification

def criar_notificacao_mensagem(sender, recipient, texto):
    if sender != recipient:
        Notification.objects.create(
            user=recipient,
            sender=sender,
            message=f"Nova mensagem de {sender.username}: {texto[:50]}...",
            notification_type='chat'
        )

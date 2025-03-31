from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from .models import Notification


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}"
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )

    def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get("type", "chat")  # Tipo padrão é "chat"
        message = data["message"]
        recipient_id = data["recipient_id"]
        sender_username = self.user.username

        recipient_group_name = f"user_{recipient_id}"

        if message_type == "chat":
            # Salvar notificação para o destinatário
            Notification.objects.create(
                user_id=recipient_id,
                message=f"Nova mensagem de {sender_username}: {message}",
                notification_type="chat"
            )

            # Enviar mensagem de chat
            async_to_sync(self.channel_layer.group_send)(
                recipient_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender_username,
                }
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender_username,
                }
            )
        elif message_type == "notification":
            # Salvar notificação genérica
            Notification.objects.create(
                user_id=recipient_id,
                message=message,
                notification_type=data.get("notification_type", "other")
            )
            # Enviar notificação
            async_to_sync(self.channel_layer.group_send)(
                recipient_group_name,
                {
                    "type": "notification.message",
                    "message": message,
                    "notification_type": data.get("notification_type", "other"),
                }
            )

    def chat_message(self, event):
        self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "sender": event["sender"],
        }))

    def notification_message(self, event):
        self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"],
            "notification_type": event["notification_type"],
        }))
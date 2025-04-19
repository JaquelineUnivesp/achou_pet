from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from .models import Notification, ChatMessage, BlockedUser

User = get_user_model()

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
        print(">> MENSAGEM RECEBIDA NO WEBSOCKET")  # DEBUG
        try:
            data = json.loads(text_data)
            message_type = data.get("type", "chat")
            message = data.get("message", "").strip()
            recipient_id = data.get("recipient_id")

            if not message or not recipient_id:
                return

            sender = self.user
            recipient = User.objects.filter(id=recipient_id).first()

            if not recipient:
                self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Usuário destinatário não encontrado."
                }))
                return

            if BlockedUser.objects.filter(blocker=recipient, blocked=sender).exists():
                self.send(text_data=json.dumps({
                    "type": "error",
                    "message": "Você foi bloqueado por este usuário."
                }))
                return

            recipient_group_name = f"user_{recipient_id}"

            if message_type == "chat":
                ChatMessage.objects.create(
                    sender=sender,
                    recipient=recipient,
                    message=message
                )

                Notification.objects.create(
                    user=recipient,
                    message=f"Nova mensagem de {sender.username}: {message}",
                    notification_type="chat"
                )

                async_to_sync(self.channel_layer.group_send)(
                    recipient_group_name,
                    {
                        "type": "chat.message",
                        "message": message,
                        "sender": sender.username,
                    }
                )

                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        "type": "chat.message",
                        "message": message,
                        "sender": sender.username,
                    }
                )

            elif message_type == "notification":
                Notification.objects.create(
                    user=recipient,
                    message=message,
                    notification_type=data.get("notification_type", "other")
                )
                async_to_sync(self.channel_layer.group_send)(
                    recipient_group_name,
                    {
                        "type": "notification.message",
                        "message": message,
                        "notification_type": data.get("notification_type", "other"),
                    }
                )

        except Exception as e:
            self.send(text_data=json.dumps({
                "type": "error",
                "message": f"Erro no servidor: {str(e)}"
            }))

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




# apps/notifications/consumers.py
from apps.notifications.utils import criar_notificacao_mensagem

async def receive(self, text_data):
    data = json.loads(text_data)
    mensagem = data['message']
    recipient_id = data['recipient_id']

    sender = self.scope['user']
    recipient = await database_sync_to_async(User.objects.get)(id=recipient_id)

    if mensagem:
        await database_sync_to_async(ChatMessage.objects.create)(
            sender=sender,
            recipient=recipient,
            message=mensagem
        )

        # cria notificação
        criar_notificacao_mensagem(sender, recipient, mensagem)

        # (e aqui você continua enviando o broadcast da mensagem)

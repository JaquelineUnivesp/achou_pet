from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q

from apps.notifications.models import Notification, ChatMessage, BlockedUser

User = get_user_model()

# 🔔 Cria uma notificação ao receber mensagem
def criar_notificacao_mensagem(sender, recipient, texto):
    if sender != recipient:
        Notification.objects.create(
            user=recipient,
            sender=sender,
            message=f"Você recebeu uma nova mensagem de {sender.username}: \"{texto[:50]}...\"",
            notification_type='chat'
        )

# 💬 Página principal do chat
@login_required
def chat_view(request):
    interacted_user_ids = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).values_list('sender', 'recipient')

    user_ids = set()
    for sender_id, recipient_id in interacted_user_ids:
        if sender_id != request.user.id:
            user_ids.add(sender_id)
        if recipient_id != request.user.id:
            user_ids.add(recipient_id)

    users = User.objects.filter(id__in=user_ids)
    blocked_ids = BlockedUser.objects.filter(blocker=request.user).values_list('blocked_id', flat=True)

    return render(request, 'notifications/chat.html', {
        'users': users,
        'blocked_ids': list(blocked_ids),
    })

# 🔔 Página de notificações
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    if request.method == "POST":
        if "mark_read" in request.POST:
            notification_id = request.POST.get("notification_id")
            notification = notifications.filter(id=notification_id).first()
            if notification:
                notification.is_read = True
                notification.save()

        elif "delete_notification_id" in request.POST:
            notification_id = request.POST.get("delete_notification_id")
            notification = notifications.filter(id=notification_id).first()
            if notification:
                notification.delete()

        return redirect('notifications:notifications')

    return render(request, 'notifications/notifications.html', {'notifications': notifications})

# 🔄 Histórico de mensagens
@login_required
@require_GET
def chat_history(request, user_id):
    current_user = request.user
    other_user = get_object_or_404(User, id=user_id)

    messages = ChatMessage.objects.filter(
        sender__in=[current_user, other_user],
        recipient__in=[current_user, other_user]
    ).order_by('timestamp')

    messages_data = [
        {
            "sender": msg.sender.username,
            "message": msg.message,
            "timestamp": msg.timestamp.strftime('%Y-%m-%d %H:%M')
        }
        for msg in messages
    ]

    return JsonResponse({"messages": messages_data})

# 🧹 Limpa mensagens enviadas para outro usuário
@login_required
@require_POST
def clear_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    ChatMessage.objects.filter(sender=request.user, recipient=other_user).delete()
    return JsonResponse({"success": True})

# 🚫 Bloquear usuário
@login_required
@require_POST
def block_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return JsonResponse({"error": "Você não pode se bloquear."}, status=400)

    BlockedUser.objects.get_or_create(blocker=request.user, blocked=other_user)
    return JsonResponse({"success": True, "message": f"Você bloqueou {other_user.username}."})

# ✅ Desbloquear usuário
@login_required
@require_POST
def unblock_user(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    BlockedUser.objects.filter(blocker=request.user, blocked=other_user).delete()
    return JsonResponse({"success": True, "message": f"Você desbloqueou {other_user.username}."})

# 👥 Listar usuários bloqueados (JSON)
@login_required
def blocked_users_list(request):
    blocked = BlockedUser.objects.filter(blocker=request.user).select_related('blocked')
    data = [{"id": b.blocked.id, "username": b.blocked.username} for b in blocked]
    return JsonResponse({"blocked_users": data})

# 👥 Página de usuários bloqueados
@login_required
def blocked_users_page(request):
    blocked_users = BlockedUser.objects.filter(blocker=request.user).select_related('blocked')
    return render(request, 'notifications/blocked_list.html', {
        'blocked_users': blocked_users
    })

# 📩 Abre ou inicia conversa com usuário específico
@login_required
def chat_with_user(request, user_id):
    if request.user.id == user_id:
        return redirect('notifications:chat')

    recipient = get_object_or_404(User, id=user_id)

    if not ChatMessage.objects.filter(
        Q(sender=request.user, recipient=recipient) |
        Q(sender=recipient, recipient=request.user)
    ).exists():
        ChatMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            message='',
            is_deleted=True
        )

    return redirect('notifications:chat')

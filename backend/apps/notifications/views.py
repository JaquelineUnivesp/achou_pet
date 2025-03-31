from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'notifications/chat.html', {'users': users})

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    if request.method == "POST" and "mark_read" in request.POST:
        notification_id = request.POST.get("notification_id")
        notification = notifications.filter(id=notification_id).first()
        if notification:
            notification.is_read = True
            notification.save()
    return render(request, 'notifications/notifications.html', {'notifications': notifications})
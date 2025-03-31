from django.urls import path
from . import views

app_name = 'notifications'
urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('notifications/', views.notifications_view, name='notifications'),
]
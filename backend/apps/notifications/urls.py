from django.urls import path
from . import views
from apps.notifications import views



app_name = 'notifications'
urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('notifications/', views.notifications_view, name='notifications'),
    path("chat/history/<int:user_id>/", views.chat_history, name="chat_history"),
path("chat/clear/<int:user_id>/", views.clear_chat, name="clear_chat"),
path("chat/block/<int:user_id>/", views.block_user, name="block_user"),
path("chat/unblock/<int:user_id>/", views.unblock_user, name="unblock_user"),
path("chat/blocked/list/", views.blocked_users_list, name="blocked_users_list"),
path("chat/bloqueados/", views.blocked_users_page, name="blocked_users_page"),
path("chat/com/<int:user_id>/", views.chat_with_user, name="chat_with_user"),

]
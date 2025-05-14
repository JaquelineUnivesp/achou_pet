# backend/apps/accounts/urls.py
app_name = 'accounts'

from django.urls import path
from . import views

from .views import (
    register_view, login_view, logout_view, password_reset_view, change_email_view, home_view,
    CustomTokenObtainPairView, RegisterUserView, CustomEmailConfirmView, profile_view, edit_profile
)
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    # API
    path('api/register/', RegisterUserView.as_view(), name='api_register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Confirmação de e-mail (apenas uma rota, fora do namespace 'api/auth/registration/')
    path('account/confirm-email/<str:key>/', CustomEmailConfirmView.as_view(), name='account_confirm_email'),

    # Frontend
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', password_reset_view, name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('change_email/', change_email_view, name='change_email'),
    path('', home_view, name='home'),
    path('profile/', profile_view, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),


]
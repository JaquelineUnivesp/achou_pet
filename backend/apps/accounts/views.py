from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailConfirmationHMAC, EmailAddress
from django.db import IntegrityError

from .models import CustomUser
from .forms import CustomUserRegistrationForm, UserProfileForm
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer

import logging
logger = logging.getLogger(__name__)
User = get_user_model()

# ===================== API Views =====================

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_confirmation(request, user, signup=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomEmailConfirmView(TemplateView):
    template_name = 'account/email_confirm.html'
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            confirmation = EmailConfirmationHMAC.from_key(kwargs['key'])
            if not confirmation:
                logger.warning(f"Chave de confirmação inválida: {kwargs['key']}")
                return self.render_to_response({'success': False})
            confirmation.confirm(request)
            user = confirmation.email_address.user
            user.is_verified = True
            user.save()
            logger.info(f"E-mail de {user.email} confirmado com sucesso")
            return self.render_to_response({'success': True})
        except Exception as e:
            logger.error(f"Erro na confirmação de e-mail: {str(e)}")
            return self.render_to_response({'success': False, 'error': str(e)})

# ===================== Frontend Views =====================

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                send_email_confirmation(request, user, signup=True)
                return redirect('accounts:login')  # ou outro nome, dependendo da sua url
            except IntegrityError:
                form.add_error('email', 'Este e-mail já está em uso.')
        # se não for válido ou erro de integridade
        return render(request, 'account/register.html', {'form': form})
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def login_view(request):
    # Se for requisição POST, o usuário está tentando fazer login
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            # Redireciona para a home ou para onde desejar após login
            return redirect('accounts:profile')  # Ajuste conforme o namespace usado
        else:
            # Login inválido, renderiza com erro
            return render(request, 'account/login.html', {
                'error': 'Credenciais inválidas. Verifique e tente novamente.',
                'email': email  # Opcional: repopula o campo de email no form
            })

    # Se for GET, apenas mostra o formulário de login
    return render(request, 'account/login.html')


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        request.session.flush()
        return redirect('accounts:login')
    return render(request, 'account/logout.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = '/account/password_reset/done/'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'

def password_reset_view(request):
    return CustomPasswordResetView.as_view()(request)

@login_required
def change_email_view(request):
    if request.method == 'POST':
        new_email = request.POST.get('email')
        if not new_email:
            return render(request, 'account/change_email.html', {'error': 'Digite um e-mail válido.'})

        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            return render(request, 'account/change_email.html', {'error': 'Este e-mail já está em uso.'})

        old_email = request.user.email
        request.user.email = new_email
        request.user.is_verified = False

        try:
            request.user.save()
            EmailAddress.objects.filter(user=request.user).exclude(email=new_email).delete()
            email_address, _ = EmailAddress.objects.get_or_create(user=request.user, email=new_email)
            email_address.send_confirmation(request)
            messages.success(request, 'E-mail atualizado! Verifique sua caixa de entrada.')
            return redirect('home')
        except Exception as e:
            logger.error(f"Erro ao salvar novo e-mail: {str(e)}")
            return render(request, 'account/change_email.html', {'error': str(e)})

    return render(request, 'account/change_email.html')

def home_view(request):
    return render(request, 'account/home.html')

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os dados informados.')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'account/edit_profile.html', {
        'form': form,
        'user': user
    })



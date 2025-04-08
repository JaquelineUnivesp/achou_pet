# backend/apps/accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .forms import CustomUserRegistrationForm  # Importar do forms.py
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.account.utils import send_email_confirmation
from allauth.account.models import EmailConfirmationHMAC
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
import logging





logger = logging.getLogger(__name__)
User = get_user_model()

# Views de API
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

# Views de Frontend
def register_view(request):
    logger.info("Acessou register_view")
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            logger.info(f"Usuário {user.email} criado com sucesso")
            try:
                send_email_confirmation(request, user, signup=True)
                logger.info(f"E-mail de confirmação enviado para {user.email}")
            except Exception as e:
                logger.error(f"Erro ao enviar e-mail para {user.email}: {str(e)}")
            return redirect('login')
        else:
            logger.warning(f"Erros no formulário: {form.errors}")
    else:
        form = CustomUserRegistrationForm()
        logger.debug("Formulário vazio criado")
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'account/login.html', {'error': 'Credenciais inválidas'})
        else:
            return render(request, 'account/login.html', {'error': 'Preencha todos os campos'})
    return render(request, 'account/login.html')

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
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
            return render(request, 'account/change_email.html', {
                'error': 'Digite um e-mail válido.'
            })

        # Verificação para evitar duplicidade
        if User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
            return render(request, 'account/change_email.html', {
                'error': 'Este e-mail já está em uso por outro usuário.'
            })

        old_email = request.user.email
        request.user.email = new_email
        request.user.is_verified = False

        try:
            request.user.save()

            # Remove e-mails antigos do usuário
            EmailAddress.objects.filter(user=request.user).exclude(email=new_email).delete()

            # Cria ou atualiza o novo email
            email_address, created = EmailAddress.objects.get_or_create(
                user=request.user,
                email=request.user.email
            )

            # Força verificação
            email_address.send_confirmation(request)

            logger.info(f"E-mail de confirmação enviado para {new_email} (anterior: {old_email})")
            messages.success(request, 'E-mail atualizado! Verifique sua caixa de entrada.')
            return redirect('home')

        except Exception as e:
            logger.error(f"Erro ao salvar novo e-mail {new_email}: {str(e)}")
            return render(request, 'account/change_email.html', {
                'error': f"Erro ao salvar ou enviar confirmação: {str(e)}"
            })

    return render(request, 'account/change_email.html')


def home_view(request):
    return render(request, 'account/home.html')



@login_required
def profile_view(request):
    user = request.user
    return render(request, 'account/profile.html', {'user': user})



@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('account:profile')
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os dados.')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'account/edit_profile.html', {'form': form})






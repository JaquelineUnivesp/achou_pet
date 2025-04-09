# backend/config/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta



IPINFO_TOKEN = os.getenv('IPINFO_TOKEN', '91e3040b4f78f5')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar variáveis do .env
load_dotenv()

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-843qjerhh!z3^v^nfo!@@yg$yb$6s3%!i(&ry)7#fxkyl__xxp'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'daphne',  # Prioridade para ASGI
    'django.contrib.admin',
    'django.contrib.auth',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Django Allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # Django REST Framework + Autenticação JWT e Tokens
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    # Apps do projeto
    'apps.accounts',
    'apps.core',
    'apps.notifications',
    'apps.pet_registration',
    'apps.search',
    'django.contrib.gis',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / '..' / 'frontend' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração dos arquivos estáticos
STATIC_URL = '/static/'  # URL base para acessar arquivos estáticos
STATICFILES_DIRS = [
    BASE_DIR / '..' / 'frontend' / 'static',  # Caminho para a pasta frontend/static/
]

# Opcional: para produção
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuração do ASGI
ASGI_APPLICATION = 'config.asgi.application'

# Configuração do Channels com Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'achou_pet'),
        'USER': os.getenv('DB_USER', 'admin'),
        'PASSWORD': os.getenv('DB_PASSWORD', '12345'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'lost_pets')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

#ACCOUNT_LOGIN_METHODS = {'email'}  # Ajustado para corrigir o aviso
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'accounts.CustomUser'

# Configuração de e-mail com Gmail SMTP
# Configurações de e-mail para desenvolvimento
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Isso vai imprimir o e-mail no console

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'alertapetpi3@gmail.com'
EMAIL_HOST_PASSWORD = 'wrlu xjef vtim nsnf'

# Configuração de CORS
CORS_ALLOW_ALL_ORIGINS = True

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
}

LOGIN_URL = '/account/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/account/login/'

# Configuração de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Configuração do Redis como cache (opcional)
CACHES = {
    'default': {
         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Configuração básica do Redis para uso geral
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# LocationIQ API Key
LOCATIONIQ_API_KEY = 'pk.227bb16be8af10a97550047d4932e148'
SETTINGS_EXPORT = ['LOCATIONIQ_API_KEY']
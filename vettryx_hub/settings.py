# vettryx_hub/settings.py

"""
Configurações do Django para o projeto VETTRYX Hub.
Baseado na estrutura com Pathlib e boas práticas de desenvolvimento.
"""

# Importações
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# --- CONFIGURAÇÃO DE PATHS ---
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR / 'apps'))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# --- CONFIGURAÇÃO DE SEGURANÇA ---
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
if os.getenv("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(os.getenv("RENDER_EXTERNAL_HOSTNAME"))

# --- CONFIGURAÇÃO DE APLICATIVOS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Autenticação de dois fatores
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    
    # Aplicativos de terceiros
    'axes',
    'storages',
    
    # Aplicativos locais

]

# --- CONFIGURAÇÃO DE MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

# --- CONFIGURAÇÃO DE ROTAS ---
ROOT_URLCONF = 'vettryx_hub.urls'

# --- CONFIGURAÇÃO DE TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            #"libraries": {
            #    "custom_filters": "templatetags.custom_filters",
            #},
        },
    },
]

# --- CONFIGURAÇÃO DE WSGI ---
WSGI_APPLICATION = 'vettryx_hub.wsgi.application'


# --- CONFIGURAÇÃO DE BANCO DE DADOS ---
USE_MYSQL = os.getenv("USE_MYSQL", "False").lower() in ("true", "1", "yes")

if USE_MYSQL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# --- CONFIGURAÇÃO DE VALIDAÇÃO DE SENHA ---
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --- CONFIGURAÇÃO DE AUTHENTICATION BACKENDS ---
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# --- CONFIGURAÇÃO DE LOGIN E REDIRECT ---
LOGIN_URL = "two_factor:login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "two_factor:login"

# --- CONFIGURAÇÃO DE INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# --- CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- CONFIGURAÇÃO DE ARQUIVOS DE MÍDIA ---
MEDIA_URL = os.getenv('SFTP_PUBLIC_URL', '/djangoApi_media/')

# --- CONFIGURAÇÃO DE ARMAZENAMENTO ---
STORAGES = {
    # 1. Arquivos Estáticos (CSS/JS) - Whitenoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
                   if not DEBUG else "django.contrib.staticfiles.storage.StaticFilesStorage",
    },

    # 2. Arquivos de Mídia (Uploads) - SFTPStorage
    "default": {
        "BACKEND": "storages.backends.sftpstorage.SFTPStorage",
        "OPTIONS": {
            "host": os.getenv('SFTP_HOST'),
            "root_path": os.getenv('SFTP_ROOT_PATH'),
            "params": {
                "port": int(os.getenv('SFTP_PORT') or 22),
                "username": os.getenv('SFTP_USER'),
                "password": os.getenv('SFTP_PASSWORD'),
                "allow_agent": False,
                "look_for_keys": False,
            },
            "file_mode": 0o644,
        },
    },
}

# --- CONFIGURAÇÃO DE SESSÕES ---
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# --- CONFIGURAÇÃO DE SEGURANÇA ---
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # SECURE_SSL_REDIRECT = True

# --- CONFIGURAÇÃO DE SEGURANÇA CONTRA FORÇA BRUTA (AXES) ---
AXES_FAILURE_LIMIT = 5 # Quantas chances o usuário tem antes de ser bloqueado?
AXES_COOLOFF_TIME = 1 # Quanto tempo (em horas) ele fica bloqueado?

# COMO O BLOQUEIO DEVE FUNCIONAR (Sintaxe Nova)
# 'username' = Bloqueia só o usuário (padrão)
# 'ip' = Bloqueia o IP todo (afeta todo mundo naquele wifi)
# 'combination_user_and_ip' = Bloqueia aquele usuário especificamente naquele IP (Mais seguro e preciso)
AXES_LOCK_OUT_BY = 'combination_user_and_ip'

# Resetar o contador se ele acertar a senha? (Sim)
AXES_RESET_ON_SUCCESS = True

# Mensagem de erro que aparece para o usuário (Opcional, mas boa prática)
AXES_LOCKOUT_TEMPLATE = None # Usa o padrão do Django ou define um template seu depois
AXES_LOCKOUT_PARAMETERS = ["username", "ip_address"]

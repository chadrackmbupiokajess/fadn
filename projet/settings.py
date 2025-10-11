"""
Django settings for projet project.
"""

from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['fadn.pythonanywhere.com', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'publication',
    'authapp',
    'tinymce',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'projet.urls'

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
        },
    },
]

WSGI_APPLICATION = 'projet.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Africa/Kinshasa'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD', default='')

LOGIN_URL = '/auth/login/'

# TinyMCE configuration
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview anchor',
    'toolbar': 'undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
    'toolbar_mode': 'floating',
}


# ========================
# CONFIGURATION MATERIAL ADMIN
# ========================

MATERIAL_ADMIN_SITE = {
    'HEADER':  'Administration FADN',              # Nom affiché en haut à gauche
    'TITLE':  'FADN',            # Titre de l’onglet navigateur
    'FAVICON':  'static/images/favicon.png',      # Icône de l’onglet (mets ton image)
    #'MAIN_BG_COLOR':  '#3f51b5',                  # Couleur principale (bleu par défaut)
    #'MAIN_HOVER_COLOR':  '#303f9f',               # Couleur survol menu
    'PROFILE_PICTURE':  'static/images/favicon.png',  # Photo profil admin
    #'PROFILE_BG':  'static/images/admin_bg.jpg',  # Image de fond profil
    'LOGIN_LOGO':  'static/images/favicon.png',      # Logo sur la page de connexion
    'LOGOUT_BG':  'static/images/logout_bg.jpg',  # Image de fond de la page de déconnexion
    'SHOW_THEMES':  True,                         # Autorise changement de thème
    'TRAY_REVERSE':  True,                        # Menu à droite ou gauche
    'NAVBAR_REVERSE':  False,                     # Barre en haut inversée ou non
    'SHOW_COUNTS':  True,
# 👇 Organisation des apps et icônes
    'APP_ICONS': {
        'publication': {
            'publication': 'mdi-book-open-page-variant',     # Publication principale
            'aproposs': 'mdi-information-outline',            # À propos
            'categories': 'mdi-folder-outline',               # Catégories
            'comments': 'mdi-comment-outline',                # Commentaires
            'contacts': 'mdi-email-outline',                  # Contacts
            'notifications': 'mdi-bell-outline',              # Notifications
        },
    },

    # 👇 Ordre et regroupement des apps (facultatif mais plus propre)
    'APP_ORDER': [
        ('publication', ['publication', 'categories', 'comments', 'contacts', 'notifications', 'aproposs']),
    ],
}

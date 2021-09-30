import os

import dotenv

dotenv.load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# TEMPLATE_DIRS = ('/home/alex/Dev/Diplom/foodgram-project-react/frontend/',)

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'api',
    'recipes',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'colorfield',
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

ROOT_URLCONF = 'grocery_assistant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # '/home/alex/Dev/Diplom/foodgram-project-react/frontend/'
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

WSGI_APPLICATION = 'grocery_assistant.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.'
    #                             'PageNumberPagination',
    # 'PAGE_SIZE': 10,
}

AUTH_USER_MODEL = 'users.User'

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
# }

DJOSER = {
    # 'USER_ID_FIELD': '#/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': '#/activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'SERIALIZERS': {
    #     'user': 'api.serializers.UserSerializer',
    # },
    # 'USER_ID_FIELD': 'email',
    'LOGIN_FIELD': 'email'
}

# AUTHENTICATION_BACKENDS = (
#     "django.contrib.auth.backends.ModelBackend",
#     # "allauth.account.auth_backends.AuthenticationBackend"
# )

# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROLES_PERMISSIONS = {
    'Users': {
        'user': ('GET',),
        'admin': ('GET',),
        'anon': ('GET', 'POST'),
    },
    'Users_me': {
        'user': ('GET', ),
        'moderator': ('GET', ),
        'anon': (None,),
    },
    'Recipe': {
        'user': ('GET', 'POST'),
        'moderator': ('GET', 'PATCH', 'DELETE', 'POST', 'PUT'),
        'anon': ('GET',),
    },
}

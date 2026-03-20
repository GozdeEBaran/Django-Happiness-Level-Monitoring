import os
from os.path import join
from configurations import Configuration
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Common(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',
                           "58acf4e1d4375b58191aeaaa95803464137852322ae86b4a04859d2480a3e668")

    ALLOWED_HOSTS = ["*"]

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Core
        'rest_framework',
        'rest_framework_simplejwt',
        'drf_spectacular',

        # Hindex App
        'hindex.utils',
        'hindex.users',
        'hindex.happiness_levels'
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

    ROOT_URLCONF = 'hindex.urls'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), 'static'))
    STATICFILES_DIRS = ['templates']
    STATIC_URL = '/static/'
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': STATICFILES_DIRS,
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'hindex.context_processor.from_settings',
                ],
            }
        },
    ]

    WSGI_APPLICATION = 'hindex.wsgi.application'
    TIER = os.getenv('TIER', 'Local').title()

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases

    DATABASES = {
        'default': {
            # 'postgres:///aesf_auth',
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', 5432),
            'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'NAME': os.getenv('DB_NAME', 'hindex'),
        }
    }

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/4.0/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_TZ = True

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    # Admin
    COLOR_MAP = {
        'Local': '#89BF04',
        'Development': '#E20000',
    }
    ENVIRONMENT_COLOR = COLOR_MAP.get(TIER, '#89BF04')

    # Django Rest Framework
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated'
        ],
        'DEFAULT_PAGINATION_CLASS': 'hindex.pagination.PageSizePageNumberPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_SCHEMA_CLASS': 'hindex.swagger_schema.AutoSchema',
    }

    # Api Documentation
    SPECTACULAR_SETTINGS = {
        'TITLE': 'Happiness Level Index',
        'DESCRIPTION': """Happiness Level API \n\n
            Note: For best experience with this API, Please append a trailing '/'.
            POST requests without it will fail to deliver posted data""",
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,
        'CAMELIZE_NAMES': True,
        'SWAGGER_UI_SETTINGS': {
            'persistAuthorization': True,
        },
    }

    SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60 * 2),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=2)
    }

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'class': 'hindex.custom_formatter.StackInfoHandler',
                'formatter': 'simple'
            }
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['django.db.backends'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }

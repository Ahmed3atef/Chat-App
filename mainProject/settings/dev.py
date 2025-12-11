from .common import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]", "*"]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS.extend([
    'debug_toolbar',
    'silk',
])

MIDDLEWARE.insert(2, "debug_toolbar.middleware.DebugToolbarMiddleware")
MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dummyDatabase',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Disable toolbar during tests to satisfy debug_toolbar.E001
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": 'mainProject.debug.show_toolbar',
    "IS_RUNNING_TESTS": False,
}


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525
DEFAULT_FROM_EMAIL= 'from@email.com'


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda reqest: True
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# # celery settings
# CELERY_BROKER_URL = 'redis://localhost:6379/1'
# CELERY_BEAT_SCHEDULE = {
#     'notify_customers': {
#         'task': 'home.tasks.notify_customers',
#         'schedule': 5,  # crontab(day_of_week=1, hour=7, minute=30),
#         'args': ['Hello World!']
#     }
# }


# configure cache backend
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/2",
        "TIMEOUT": 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

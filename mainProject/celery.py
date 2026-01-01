import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mainProject.settings.dev')
celery = Celery('mainProject')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

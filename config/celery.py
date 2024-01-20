import os
from celery import Celery

# Set default settings from Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically download tasks from all registered Django apps
app.autodiscover_tasks()

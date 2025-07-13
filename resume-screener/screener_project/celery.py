# screener_project/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screener_project.settings')
app = Celery('screener_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
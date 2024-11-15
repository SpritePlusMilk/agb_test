import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Фоновая задача по обработке Xml-файла с данными о продуктах
    'analyze-products-task': {
        'task': 'parser.tasks.analyze_products_task',
        'schedule': crontab(hour='12', minute='0'),
    },
}

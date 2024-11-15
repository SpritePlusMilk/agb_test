from celery import shared_task
from django.conf import settings
from tools import analyze_products


@shared_task
def analyze_products_task() -> None:
    if not settings.DEBUG:
        pass
    else:
        analyze_products()

from django.conf import settings
from huey import crontab

from .tools import analyze_products

huey = settings.HUEY


@huey.periodic_task(crontab(minute='*/1'))
def analyze_products_task() -> None:
    if not settings.DEBUG:
        pass
    else:
        analyze_products()

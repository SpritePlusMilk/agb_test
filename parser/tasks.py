from django.conf import settings
from huey import crontab

from .tools import analyze_products

huey = settings.HUEY


@huey.periodic_task(crontab(hour=12, minute=0))
def analyze_products_task() -> None:
    if settings.DEBUG:
        pass
    else:
        analyze_products()

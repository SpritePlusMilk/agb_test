from celery import shared_task


@shared_task
def analyze_products_data() -> None:
    pass

import asyncio
import logging

from django.conf import settings
from django.utils.timezone import now
from huey import crontab

from parser import models

from .openai import request_llm_analysis
from .xml_parsing import EmptyFile, InvalidResponse, get_xml_data, process_xml_data

logger = logging.getLogger('xml_data_logger')
huey = settings.HUEY


async def get_and_process_data(source: models.Source) -> None:
    xml_data = await get_xml_data(source)
    try:
        xml_file = await process_xml_data(source, xml_data)  # noqa
    except (InvalidResponse, EmptyFile):
        logger.warning(f'{now()}: ответ от {source.url} не является xml-файлом/ содержит xml-файл неверного формата')
        return
    await request_llm_analysis(xml_file)


async def process_sources() -> None:
    async with asyncio.TaskGroup() as tg:
        async for source in models.Source.objects.filter(is_active=True):
            tg.create_task(coro=get_and_process_data(source))


@huey.periodic_task(crontab(hour=12, minute=0))
def analyze_products() -> None:
    if settings.DEBUG:
        pass
    else:
        asyncio.run(process_sources())

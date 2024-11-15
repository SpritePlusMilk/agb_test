import asyncio
import logging

import aiohttp

from parser import models

logger = logging.getLogger('xml_data_logger')


async def get_xml_data() -> str:
    async with aiohttp.ClientSession() as session, session.get('http://127.0.0.1:8000/ex') as response:  #todo тестовый эндпоинт для получения xml
        logger.warning('Status:', response.status)
        logger.warning('Content-type:', response.headers['content-type'])

        html = await response.text()
        logger.warning(f'Получен xml-файл: {html}')
        return html


async def process_xml_data(xml_data: str):
    print(xml_data)
    a = await models.Xml.objects.acreate()
    return a


async def get_and_process_data():
    xml_data = await get_xml_data()
    xml_file = await process_xml_data(xml_data)


def analyze_products():
    asyncio.run(get_and_process_data())

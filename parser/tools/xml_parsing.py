import logging
from typing import TYPE_CHECKING

import aiohttp
from bs4 import BeautifulSoup, NavigableString
from django.utils.timezone import now

from parser import models
from parser.tools import retry

from .exceptions import EmptyFile, InvalidResponse

if TYPE_CHECKING:
    from bs4 import Tag

logger = logging.getLogger('xml_data_logger')


@retry(delay=5, delay_step=10, max_delay=60)
async def get_xml_data(source: models.Source) -> str:
    async with aiohttp.ClientSession() as session, session.get(source.url) as response:
        html = await response.text()
        logger.warning(f'{now()}: От {source.url} получен xml-файл:\n{html}')
        return html


def get_nested_tag_content(tag: 'Tag', nested_tag: str, default: any = '') -> str:
    if tag:
        tag_data = tag.find(nested_tag)
        return tag_data.text if tag.text else default
    return default


async def process_xml_data(source: models.Source, xml_data: str) -> models.Xml:
    soup = BeautifulSoup(xml_data, 'xml')
    if main_tag := soup.find('sales_data'):
        xml_date = main_tag.get('date', now().date())
        xml_file = await models.Xml.objects.acreate(source=source, date=xml_date)

        if products := main_tag.find('products'):
            for product_ in [content for content in products.contents if type(content) is not NavigableString]:
                product_data = {
                    'name': get_nested_tag_content(product_, 'name'),
                    'quantity': get_nested_tag_content(product_, 'quantity'),
                    'price': get_nested_tag_content(product_, 'price'),
                    'category': get_nested_tag_content(product_, 'category'),
                }
                await models.Product.objects.acreate(xml_file=xml_file, **product_data)
            return xml_file

        raise EmptyFile('Полученный xml-файл не содержит списка продуктов')

    raise InvalidResponse(
        'Полученный ответ не является xml-файлом, либо содержимое xml-файла имеет некорректную стуктуру'
    )

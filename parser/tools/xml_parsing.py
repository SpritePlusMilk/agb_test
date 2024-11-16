import logging
from typing import TYPE_CHECKING

import aiohttp
from bs4 import BeautifulSoup, NavigableString
from django.utils.timezone import now

from parser import models

if TYPE_CHECKING:
    from bs4 import Tag

logger = logging.getLogger('xml_data_logger')


async def get_xml_data(source: models.Source) -> str:
    async with aiohttp.ClientSession() as session, session.get(source.url) as response:
        logger.warning('Status:', response.status)
        logger.warning('Content-type:', response.headers['content-type'])

        html = await response.text()
        logger.warning(f'{now()}: получен xml-файл: {html}')
        return html


def get_nested_tag_content(tag: 'Tag', nested_tag: str, default: any = '') -> str:
    if tag:
        tag_data = tag.find(nested_tag)
        return tag_data.text if tag.text else default
    return default


async def process_xml_data(source: models.Source, xml_data: str) -> models.Xml:
    soup = BeautifulSoup(xml_data, 'xml')
    main_tag = soup.find('sales_data')
    xml_date = main_tag.get('date', now().date())
    xml_file = await models.Xml.objects.acreate(source=source, date=xml_date)

    products = [content for content in main_tag.find('products').contents if type(content) is not NavigableString]
    for product in products:
        product_data = {
            'name': get_nested_tag_content(product, 'name'),
            'quantity': get_nested_tag_content(product, 'quantity'),
            'price': get_nested_tag_content(product, 'price'),
            'category': get_nested_tag_content(product, 'category'),
        }
        await models.Product.objects.acreate(xml_file=xml_file, **product_data)

    return xml_file

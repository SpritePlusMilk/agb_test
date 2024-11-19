from bs4 import BeautifulSoup
from django.test import TestCase

from parser.models import Product
from parser.tests import factories
from parser.tools.exceptions import EmptyFile, InvalidResponse
from parser.tools.xml_parsing import get_nested_tag_content, process_xml_data


class GetNestedTagContentTest(TestCase):
    def test_get_nested_tag_content_existing_tag(self) -> None:
        html = '<parent><child>Content</child></parent>'
        tag = BeautifulSoup(html, 'xml').find('parent')
        result = get_nested_tag_content(tag, 'child')

        self.assertEqual(result, 'Content')

    def test_get_nested_tag_content_non_existing_tag(self) -> None:
        html = '<parent></parent>'
        tag = BeautifulSoup(html, 'xml').find('parent')
        result = get_nested_tag_content(tag, 'child', default='Default Value')

        self.assertEqual(result, 'Default Value')

    def test_get_nested_tag_content_empty_tag(self) -> None:
        html = '<parent><child></child></parent>'
        tag = BeautifulSoup(html, 'xml').find('parent')
        result = get_nested_tag_content(tag, 'child', default='Default Value')

        self.assertEqual(result, 'Default Value')


class ProcessXmlDataTest(TestCase):
    def setUp(self) -> None:
        self.source = factories.Source()

    async def test_process_xml_data_success(self) -> None:
        xml_data = """
            <sales_data date="2024-01-01">
                <products>
                    <product>
                        <name>Product 1</name>
                        <quantity>10</quantity>
                        <price>100</price>
                        <category>Category 1</category>
                    </product>
                </products>
            </sales_data>
        """

        xml_file = await process_xml_data(self.source, xml_data)

        self.assertEqual(xml_file.source, self.source)
        self.assertEqual(await Product.objects.acount(), 1)

    async def test_process_xml_data_empty_file(self) -> None:
        xml_data = '<sales_data></sales_data>'

        with self.assertRaises(EmptyFile):
            await process_xml_data(self.source, xml_data)

    async def test_process_xml_data_invalid_response(self) -> None:
        xml_data = '<invalid_response></invalid_response>'

        with self.assertRaises(InvalidResponse):
            await process_xml_data(self.source, xml_data)

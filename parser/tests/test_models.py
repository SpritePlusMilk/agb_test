from django.db.utils import IntegrityError
from django.test import TestCase

from parser import models
from parser.tests import factories
from parser.views import serializers


class SourceTest(TestCase):
    def setUp(self) -> None:
        self.source = factories.Source(is_active=True)

    def test_source_str(self) -> None:
        """Проверка __str__()"""
        self.assertEqual(str(self.source), f'Источник {self.source.url[:20]} (активный: {self.source.is_active})')

    def test_unique_url(self) -> None:
        """Проверка на уникальность url источника xml-файлов"""
        models.Source.objects.create(url='Unique source')
        with self.assertRaises(IntegrityError):
            models.Source.objects.create(url='Unique source')


class XmlTest(TestCase):
    def setUp(self) -> None:
        self.xml_file = factories.Xml()

    def test_xml_str(self) -> None:
        """Проверка __str__()"""
        self.assertEqual(str(self.xml_file), f'Xml-файл от {self.xml_file.date}')


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.product = factories.Product()

    def test_product_str(self) -> None:
        """Проверка __str__()"""
        self.assertEqual(
            str(self.product),
            f'Продукт "{self.product.name} ({self.product.category}),'
            f' {self.product.quantity} шт., {self.product.price} руб.',
        )

    def test_negative_quantity(self) -> None:
        """Проверка на невозможность сохранить продукт с негативным количеством проданных экземпляров"""
        data = factories.create_data(models.Product, serializers.ProductSerializer, factories.Product)
        data['xml_file'] = models.Xml.objects.get(id=data['xml_file'])
        data['quantity'] = -1
        with self.assertRaises(IntegrityError):
            models.Product.objects.create(**data)


class SalesAnalysisTest(TestCase):
    def setUp(self) -> None:
        self.analysis = factories.SalesAnalysis()

    def test_analysis_str(self) -> None:
        """Проверка __str__()"""
        self.assertEqual(
            str(self.analysis),
            f'Анализ продаж от {self.analysis.xml_file.date}',
        )

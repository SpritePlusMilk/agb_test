from django.core.validators import MinValueValidator
from django.db import models

from parser.consts import CATEGORY_CHOICES


class Xml(models.Model):
    date = models.DateField('Дата', help_text='Дата получения xml с данными о продуктах', auto_now_add=True)

    class Meta:
        verbose_name = 'Xml-файл'
        verbose_name_plural = 'Xml-файлы'
        indexes = [
            models.Index(fields=['date']),
        ]

    def __str__(self) -> str:
        return f'Xml-файл от {self.date}'


class Product(models.Model):
    xml_file = models.ForeignKey('Xml', verbose_name='Xml-файл', related_name='products', on_delete=models.CASCADE)

    name = models.CharField('Наименование', max_length=255)
    quantity = models.IntegerField(
        'Количество',
        validators=((MinValueValidator(0, 'Количество товаров не может быть отрицательным')),),
    )
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)
    category = models.CharField('Категория', max_length=255, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f'Продукт "{self.name} ({self.category}), {self.quantity} шт., {self.price} руб.'


class AnalysisResponse(models.Model):
    text = models.TextField('Текст анализа продаж', help_text='Ответ LLM')
    xml_file = models.OneToOneField('Xml', verbose_name='Xml-файл', related_name='analysis', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Анализ продаж'
        verbose_name_plural = 'Анализ продаж'

    def __str__(self) -> str:
        return f'Анализ продаж от {self.xml_file.date}'

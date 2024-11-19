from django.db import models

from parser.consts import CATEGORY_CHOICES


class Source(models.Model):
    url = models.URLField('URL-адрес', unique=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Источник для получения xml-файла'
        verbose_name_plural = 'Источники для получения xml-файлов'

    def __str__(self) -> str:
        return f'Источник {self.url[:20]} (активный: {self.is_active})'


class Xml(models.Model):
    date = models.DateField('Дата', help_text='Дата получения xml с данными о продуктах')
    source = models.ForeignKey('Source', verbose_name='Источник', related_name='xml_files', on_delete=models.CASCADE)

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
    quantity = models.IntegerField('Количество', default=0)
    price = models.DecimalField('Стоимость', max_digits=8, decimal_places=2)
    category = models.CharField('Категория', max_length=255, choices=CATEGORY_CHOICES)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gte=0), name='quantity_is_positive'),
        ]

    def __str__(self) -> str:
        return f'Продукт "{self.name} ({self.category}), {self.quantity} шт., {self.price} руб.'


class SalesAnalysis(models.Model):
    xml_file = models.OneToOneField(
        'Xml', verbose_name='Связанный xml-файл', related_name='analysis', on_delete=models.CASCADE
    )
    prompt = models.TextField('Текст запроса на анализ продаж', help_text='Промпт для LLM')
    text = models.TextField('Текст анализа продаж', help_text='Ответ LLM')

    class Meta:
        verbose_name = 'Результат анализ продаж'
        verbose_name_plural = 'Результаты анализов продаж'

    def __str__(self) -> str:
        return f'Анализ продаж от {self.xml_file.date}'

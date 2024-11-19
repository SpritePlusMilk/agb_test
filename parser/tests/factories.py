from datetime import datetime
from typing import TYPE_CHECKING

import factory
from django.contrib.auth.models import User
from factory import fuzzy
from faker import Factory

from parser import models
from parser.consts import CATEGORY_CHOICES

if TYPE_CHECKING:
    from django.db.models import Model
    from factory.django import DjangoModelFactory
    from rest_framework.serializers import ModelSerializer


factory_ru = Factory.create(locale='ru_Ru')


class User(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: factory_ru.user_name())
    email = factory.Sequence(lambda n: factory_ru.email())
    first_name = factory.Sequence(lambda n: factory_ru.first_name())
    last_name = factory.Sequence(lambda n: factory_ru.last_name())

    class Meta:
        model = User


class Source(factory.django.DjangoModelFactory):
    url = factory.Sequence(lambda n: factory_ru.uri())
    is_active = factory.Sequence(lambda n: factory_ru.pybool())

    class Meta:
        model = models.Source


class Xml(factory.django.DjangoModelFactory):
    date = fuzzy.FuzzyDate(datetime(2024, 1, 1), datetime(2024, 12, 31))
    source = factory.SubFactory(Source)

    class Meta:
        model = models.Xml


class Product(factory.django.DjangoModelFactory):
    xml_file = factory.SubFactory(Xml)
    name = factory.Sequence(lambda n: factory_ru.word())
    quantity = fuzzy.FuzzyInteger(1, 1000)
    price = fuzzy.FuzzyDecimal(1, 1000)
    category = fuzzy.FuzzyChoice(i[0] for i in CATEGORY_CHOICES)

    class Meta:
        model = models.Product


class SalesAnalysis(factory.django.DjangoModelFactory):
    xml_file = factory.SubFactory(Xml)
    prompt = factory.Sequence(lambda n: factory_ru.text())
    text = factory.Sequence(lambda n: factory_ru.text())

    class Meta:
        model = models.SalesAnalysis


def create_data(
    model: 'Model', serializer: 'ModelSerializer', factory_: 'DjangoModelFactory', *args: list, **kwargs: dict
) -> dict:
    temp_object = factory_(*args, **kwargs)
    data = dict(serializer(temp_object).data)
    model.objects.get(id=data.pop('id')).delete()

    return data

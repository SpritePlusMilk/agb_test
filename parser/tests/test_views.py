from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from parser.models import Source
from parser.tests import factories
from parser.views import serializers

factory_ru = Factory.create(locale='ru_Ru')


class TestApi(APITestCase):
    def setUp(self) -> None:
        self.password = factory_ru.password()
        self.user = factories.User()
        self.user.set_password(self.password)
        self.user.save()

        Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

        self.source = factories.Source(is_active=True)
        self.initial_source_count = Source.objects.count()

    def test_list(self) -> None:
        url = reverse('parser:sources-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.initial_source_count)

    def test_list_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detail(self) -> None:
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.source.id)
        self.assertEqual(response.data['url'], self.source.url)
        self.assertEqual(response.data['is_active'], self.source.is_active)

    def test_detail_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create(self) -> None:
        url = reverse('parser:sources-list')
        data = factories.create_data(Source, serializers.SourceSerializer, factories.Source)

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(Source.objects.count(), self.initial_source_count)
        self.assertEqual(response.data['url'], data['url'])
        self.assertEqual(response.data['is_active'], data['is_active'])

    def test_create_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-list')
        data = factories.create_data(Source, serializers.SourceSerializer, factories.Source)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_url(self) -> None:
        url = reverse('parser:sources-list')
        data = {'url': 'not a url at all'}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self) -> None:
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})
        data = factories.create_data(Source, serializers.SourceSerializer, factories.Source)

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], data['url'])
        self.assertEqual(response.data['is_active'], data['is_active'])

    def test_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})

        response = self.client.put(url, factories.create_data(Source, serializers.SourceSerializer, factories.Source))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update(self) -> None:
        source_before_update = serializers.SourceSerializer(self.source).data
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})
        data = {
            'url': factories.create_data(Source, serializers.SourceSerializer, factories.Source)['url'],
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], data['url'])
        self.assertEqual(response.data['is_active'], source_before_update['is_active'])

    def test_partial_update_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})

        response = self.client.patch(url, factories.create_data(Source, serializers.SourceSerializer, factories.Source))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete(self) -> None:
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertLess(Source.objects.count(), self.initial_source_count)

    def test_delete_unauthorized(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='')
        url = reverse('parser:sources-detail', kwargs={'pk': self.source.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Source.objects.count(), self.initial_source_count)

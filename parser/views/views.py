from typing import TYPE_CHECKING

from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet

from parser.filters import SourceFilter
from parser.models import Source
from parser.serializers import SourceSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter


def example_view(request: 'Request') -> HttpResponse:
    return HttpResponse(open('preview.xml').read(), content_type='text/xml')

from django_filters import rest_framework

from parser.models import Source


class SourceFilter(rest_framework.FilterSet):
    class Meta:
        model = Source
        fields = '__all__'

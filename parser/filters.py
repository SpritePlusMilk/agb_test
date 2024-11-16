from django_filters import rest_framework


class SourceFilter(rest_framework.FilterSet):
    class Meta:
        fields = '__all__'

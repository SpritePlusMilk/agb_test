from rest_framework import serializers


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

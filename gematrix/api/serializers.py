# Date: 22.10.2019 15:57
# Author: MaximRaduntsev

from rest_framework import serializers
from api.models import DataPoint, Producer, Dataset


class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('id', 'x_data', 'y_value')
        depth = 1


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'title', 'source_url')


class DatasetSerializer(serializers.ModelSerializer):
    source = ProducerSerializer()
    data_point = serializers.SerializerMethodField('get_data_point')

    class Meta:
        model = Dataset
        fields = ('id', 'title', 'created', 'updated', 'data_point', 'source')
        read_only_fields = ['created', 'updated']

    def get_data_point(self, obj):
        serializer = DataPointSerializer(DataPoint.objects.all(), many=True, read_only=True)
        return serializer.data

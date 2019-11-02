# Date: 22.10.2019 15:57

from rest_framework import serializers
from api.models import DataPoint, Producer, Dataset, Core


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


class FeedEventsSerializer(DatasetSerializer):
    datePeriodFrom = serializers.SerializerMethodField('get_period_from')
    datePeriodTo = serializers.SerializerMethodField('get_period_to')
    dataPointsCount = serializers.SerializerMethodField('get_datapoints_count')

    class Meta:
        model = Dataset
        fields = ('id', 'title', 'created',
                  'datePeriodFrom', 'datePeriodTo', 'dataPointsCount', 'source')
        read_only_fields = ['created']

    def get_period_from(self, obj):
        s = DataPoint.objects.distinct().order_by('x_data').values('x_data')[0]
        return s

    def get_period_to(self, obj):
        s = DataPoint.objects.distinct().order_by('x_data').values('x_data').reverse()[0]
        return s

    def get_datapoints_count(self, obj):
        num = DataPoint.get_count_all()
        return num

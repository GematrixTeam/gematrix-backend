# Date: 22.10.2019 15:57

from rest_framework import serializers
from api.models import GematrixData, GematrixSource, GematrixDatasets, Core


class GematrixSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GematrixSource
        fields = ('name', 'source_name')


class GematrixDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GematrixData
        fields = [
            # 'id',
            # 'dataset',
            'x_data',
            'y_value',
        ]
        read_only_fields = ('id', 'dataset',)


class GematrixDatasetsSerializer(serializers.ModelSerializer):
    source = GematrixSourceSerializer()
    data_point = serializers.SerializerMethodField('get_data_point')

    class Meta:
        model = GematrixDatasets
        fields = [
            # 'id',
            'name',
            'time_created',
            'time_updated',
            'data_point',
            'source'
        ]

    def get_data_point(self, obj):
        serializer = GematrixDataSerializer(GematrixData.objects.all(), many=True)
        return serializer.data


class GematrixDatasetsInlineSerializer(serializers.ModelSerializer):
    source = GematrixSourceSerializer(read_only=False)
    data_point = GematrixDataSerializer(read_only=False, many=True)

    class Meta:
        model = GematrixDatasets
        fields = [
            'id',
            'name',
            'time_created',
            'time_updated',
            'data_point',
            'source',
        ]
        read_only_fields = ('id', 'time_created', 'time_updated',)

    def create(self, validated_data):
        data_point = validated_data.pop('data_point')
        source_data = validated_data.pop('source')
        if source_data:
            source = GematrixSource.objects.get_or_create(**source_data)[0]
            validated_data['source'] = source

        dataset = GematrixDatasets.objects.create(**validated_data)

        for data in data_point:
            GematrixData.objects.create(**data, dataset=dataset)

        return dataset


class FeedEventsSerializer(GematrixDatasetsSerializer):
    datePeriodFrom = serializers.SerializerMethodField('get_period_from')
    datePeriodTo = serializers.SerializerMethodField('get_period_to')
    dataPointsCount = serializers.SerializerMethodField('get_datapoints_count')

    class Meta:
        model = GematrixDatasets
        fields = ('id', 'name', 'time_created',
                  'datePeriodFrom', 'datePeriodTo', 'dataPointsCount', 'source')
        read_only_fields = ['time_created']

    def get_period_from(self, obj):
        s = GematrixData.objects.distinct().order_by('x_data').values('x_data')[0]
        return s

    def get_period_to(self, obj):
        s = GematrixData.objects.distinct().order_by('x_data').values('x_data').reverse()[0]
        return s

    def get_datapoints_count(self, obj):
        num = GematrixData.get_count_all()
        return num

# Date: 22.10.2019 15:57

from rest_framework import serializers
from api.models import GematrixData, GematrixSource, GematrixDatasets, GematrixTags


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
            'timestamp',
            'value',
        ]
        read_only_fields = ('id', 'dataset',)


class GematrixTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GematrixTags
        fields = ['name']


class GematrixDatasetSerializer(serializers.ModelSerializer):
    source = GematrixSourceSerializer(read_only=False)
    data_point = GematrixDataSerializer(read_only=False, many=True)
    gematrix_tags = GematrixTagsSerializer(read_only=False, many=True)

    class Meta:
        model = GematrixDatasets
        fields = [
            'id',
            'name',
            'time_created',
            'time_updated',
            'data_point',
            'source',
            "gematrix_tags",
        ]
        read_only_fields = ('id', 'time_created', 'time_updated',)

    def create(self, validated_data):
        data_point = validated_data.pop('data_point')
        source_data = validated_data.pop('source')
        tags_data = validated_data.pop('gematrix_tags')

        if source_data:
            source = GematrixSource.objects.get_or_create(**source_data)[0]
            validated_data['source'] = source

        dataset = GematrixDatasets.objects.create(**validated_data)

        for data in data_point:
            GematrixData.objects.create(**data, dataset=dataset)
        for tag_data in tags_data:
            dataset.gematrix_tags.create(**tag_data)

        return dataset


class FeedEventsSerializer(serializers.ModelSerializer):
    datePeriodFrom = serializers.SerializerMethodField('get_period_from')
    datePeriodTo = serializers.SerializerMethodField('get_period_to')
    dataPointsCount = serializers.SerializerMethodField('get_datapoints_count')
    source = GematrixSourceSerializer()

    class Meta:
        model = GematrixDatasets
        fields = ('id', 'name', 'time_created',
                  'datePeriodFrom', 'datePeriodTo', 'dataPointsCount', 'source')
        read_only_fields = ['time_created']

    def get_period_from(self, obj):
        s = GematrixData.objects.distinct().order_by('timestamp').values('timestamp')[0]
        return s

    def get_period_to(self, obj):
        s = GematrixData.objects.distinct().order_by('timestamp').values('timestamp').reverse()[0]
        return s

    def get_datapoints_count(self, obj):
        num = GematrixData.get_count_all()
        return num

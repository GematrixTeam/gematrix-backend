from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.get_data_sample import feed_datasample, datasample

# Create your views here.

from api.models import GematrixDatasets
from api.serializers import FeedEventsSerializer, GematrixDatasetSerializer


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def get_post_json(request):
    # curl -X POST http://localhost:8000/api/upload-data/
    # curl -X GET http://localhost:8000/api/upload-data/
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_users_feed(request):
    # curl -X GET http://localhost:8000/api/users/feed
    if request.method == 'GET':
        return JsonResponse(feed_datasample)


@api_view(['GET'])
def get_data_by_id(requset, slug):
    # curl -X GET http://localhost:8000/api/v1/datasets/{dataset_id}
    return JsonResponse(datasample)


class GematrixDatasetsViewSet(viewsets.ModelViewSet):
    serializer_class = GematrixDatasetSerializer
    queryset = GematrixDatasets.objects.all()


class FeedEventsView(viewsets.ViewSet):

    def list(self, request, n=10):
        # curl -X GET http://localhost:8000/api/v1/feed/
        queryset = reversed(GematrixDatasets.objects.order_by('time_updated')[:n])
        serializer = FeedEventsSerializer(queryset, many=True)
        return Response(serializer.data)

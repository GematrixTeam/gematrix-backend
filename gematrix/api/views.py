from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse




# Create your views here.

@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def get_post_json(request):
    # curl -X POST http://localhost:8000/api/upload-data/
    # curl -X GET http://localhost:8000/api/upload-data/
    if request.method == 'GET':
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'POST':
        return Response(status=status.HTTP_201_CREATED)


datasample = {
    "feed": [
        {"id": "testb09199c62bcf9418ad846dd0e4bbdfc6ee4b",
         "timestamp": "2019-10-23T18:00:43.511Z",
         "title": "Some extremely valuable data",
         "datePeriodFrom": "2017-10-23T18:00:43.511Z",
         "datePeriodTo": "2018-10-23T18:00:43.511Z",
         "dataPointsCount": 1024,
         "source": {"name": "Eurostat",
                    "url": "https://ec.europa.eu/eurostat/estat-navtree-portlet-prod"}
         }
    ]
}


@api_view(['GET'])
def get_users_feed(request):
    # curl -X GET http://localhost:8000/api/users/feed
    if request.method == 'GET':
        return JsonResponse(datasample)

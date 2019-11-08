# Date: 25.10.2019 23:02

from django.urls import path, include

from rest_framework import routers

from api.views import FeedEventsView, GematrixDatasetsViewSet

router = routers.DefaultRouter()
router.register(r'feed', FeedEventsView, 'FeedEvents')
router.register(r'datasets', GematrixDatasetsViewSet, 'Datasets')

app_name = "api"

urlpatterns = [
    path('', include(router.urls))
]

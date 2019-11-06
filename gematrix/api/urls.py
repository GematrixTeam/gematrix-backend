# Date: 25.10.2019 23:02

from django.urls import path, include

from rest_framework import routers

from api.views import get_data_by_id, get_post_json, get_users_feed, \
    FeedEventsView, GematrixDatasetsViewSet

router = routers.DefaultRouter()
router.register(r'feed', FeedEventsView, 'LastNEvents')
router.register(r'dataset', GematrixDatasetsViewSet, 'Dataset')

app_name = "api"

urlpatterns = [
    path('', include(router.urls)),
    path('datasets/<slug:slug>/', get_data_by_id, name=""),
    path('upload-data/', get_post_json, name='get_post_json'),
    path('users/feed/', get_users_feed, name='get_users_feed'),
]

# Date: 25.10.2019 23:02

from django.urls import path, include

from rest_framework import routers

from api.views import DataPointView, DatasetView,\
    get_data_by_id, get_post_json, get_users_feed,\
    FeedEventsView

router = routers.DefaultRouter()
router.register(r'datapoints', DataPointView, basename='user')
router.register(r'datasets', DatasetView, basename='user')
router.register(r'feed', FeedEventsView, basename='user')

app_name = "api"

urlpatterns = [
    path('', include(router.urls)),
    path('datasets/<slug:slug>/', get_data_by_id, name=""),
    path('datasets/', get_post_json, name='get_post_json'),
    path('users/feed/', get_users_feed, name='get_users_feed'),
]

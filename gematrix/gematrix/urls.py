"""gematrix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import routers
from api.views import get_post_json, get_users_feed, get_data_by_id

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'admin/', admin.site.urls),
    re_path(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^api/upload-data', get_post_json, name='get_post_json'),
    re_path(r'^api/users/feed', get_users_feed, name='get_users_feed'),
    path('api/v1/datasets/<slug:slug>', get_data_by_id)
]

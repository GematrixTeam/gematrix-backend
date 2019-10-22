from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
import json


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

jsonsample = json.dumps(datasample)



# initialize the APIClient app
client = Client()

class GetTest(TestCase):
    """ Test module """

    def test_me(self):
        # get API response
        response_get = client.get(reverse('get_post_json'))
        response_post = client.post(reverse('get_post_json'))

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

    def test_users_feed(self):
        # get API response
        response_get = client.get(reverse('get_users_feed'))
        data = json.loads(response_get.content)

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
        self.assertEqual(data, datasample)




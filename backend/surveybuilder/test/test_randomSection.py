import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from surveybuilder.serializers import RadomSectionsSerializer
from surveybuilder.models import Survey, RandomSections
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RadomSectionTestCase(APITestCase):

    def setUp(self):
        user=User.objects.create(id=2000, username="testUser")
        Survey.objects.create(id=2000, researcher=user)

    def test_create_randomSection(self):
        response = self.client.post("/api/randomSections?order=1&survey_id=2000",format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = {'survey': 2000, 'display': 1, 'startWith': 1, 'endWith': 1, 'index': 0}
        self.assertEqual(response.json(), expected)

    def test_get_randomSection(self):
        self.client.post("/api/randomSections?order=1&survey_id=2000",format='json')
        response2 = self.client.get("/api/randomSections/2000")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        expected = [{'display': 1, 'startWith': 1, 'endWith': 1, 'index': 0}]
        self.assertEqual(response2.json(), expected)


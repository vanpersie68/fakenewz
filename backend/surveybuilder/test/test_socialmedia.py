import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

class SocialMediaMetadataTestCase(APITestCase):
    # Testing suite for all functions related to the Social Media Question type.
    def test_fetchmetadata(self):
        data = {"link": "https://www.theonion.com/signs-your-landlord-is-definitely-taking-advantage-of-y-1847697497"}
        response = self.client.post("/api/article", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 5)

    def test_fetchVideoData(self):
        data={'link':'https://www.youtube.com/watch?v=nIVgberBC5Y'}
        response = self.client.get("/api/video",data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)

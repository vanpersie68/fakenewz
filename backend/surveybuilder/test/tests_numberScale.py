import os, django

from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class TextEntryTestCase(APITestCase):

    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_patch_title(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')

        # Creates a new question
        data_question = {"type": "Number scale", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')

        # update minTitle
        data_patch = {'minTitle': "test"}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['minTitle'], "test")

        # update minTitleOn state to false
        data_patch_false = {'minTitleOn': 0}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch_false,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['minTitleOn'], 0)
        self.assertEqual(patch_response.json()['minTitle'], "")

        # update middleTitle
        data_patch = {'middleTitle': "test"}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['middleTitle'], "test")

        # update midTitleOn state to false
        data_patch_false = {'midTitleOn': 0}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch_false,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['midTitleOn'], 0)
        self.assertEqual(patch_response.json()['middleTitle'], "")

        # update maxTitle
        data_patch = {'maxTitle': "test"}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['maxTitle'], "test")

        # update maxTitleOn state to false
        data_patch_false = {'maxTitleOn': 0}
        patch_response = self.client.patch(f"/api/questions/numberScale/{question_response.json()['id']}",
                                           data_patch_false,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['maxTitleOn'], 0)
        self.assertEqual(patch_response.json()['maxTitle'], "")
        self.client.delete(f"/api/surveys/{survey_response.json()['id']}")

    def test_exception(self):
        # try to get question information which is not exist
        patch_response = self.client.patch(f"/api/questions/numberScale/10")
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

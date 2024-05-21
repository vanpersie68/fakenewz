import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class BlockTestCase(APITestCase):
    # Testing suite for all functions related to the entity Block

    def setUp(self):
        User.objects.create(id=2000,username="testUser")

    def test_nonexistent_block(self):
        # Tests that non-existent block URL returns 404 code

        response = self.client.get('/api/blocks/200')
        # as we haven't created any blocks, this should return a 404 error
        self.assertEqual(response.status_code, 404)
        # check the error message given matches what we expect
        expected_message = {'Message': 'The block can\'t be found.'}
        self.assertEqual(response.json(), expected_message)

    def test_nonexistent_block_questions(self):
        # Tests that non-existent block URL returns 404 code

        response = self.client.get('/api/blocks/200/questions')
        # as we haven't created any blocks, this should return a 404 error
        self.assertEqual(response.status_code, 404)
        # check the error message given matches what we expect
        expected_message = {'Message': 'The block can\'t be found.'}
        self.assertEqual(response.json(), expected_message)

    def test_blockCreate(self):
        # Tests that a block can be created

        # Creates a new survey
        data = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        response = self.client.post("/api/surveys", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Creates a block for the survey
        data = {"title": "block number one!", "order": 1}
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data, format='json')
        expected = {"id": response_2.json()['id'],"title": "block number one!", "order": 1, "survey": response_2.json()['survey'], "description": ''}
        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_2.json()), 5)
        self.assertEqual(response_2.json(), expected)

        # Check that the survey has greater than zero blocks.
        response_3 = self.client.get(f"/api/surveys/{response.json()['id']}/blocks")
        self.assertGreater(len(response_3.json()), 0)

    def test_getIDblock(self):
        # Tests if you can fetch a block by ID

        # Creates a new survey and a block
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')

        # Check that the block exists
        response_3 = self.client.get(f"/api/blocks/{response_2.json()['id']}")
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_3.json()), 5)

    def test_deleteBlock(self):
        # Tests if you can delete a block by ID

        # Creates a new survey and a block
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')

        # Delete the block
        response_3 = self.client.delete(f"/api/blocks/{response_2.json()['id']}")
        self.assertEqual(response_3.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the block doesn't exist
        response_4 = self.client.get(f"/api/blocks/{response_2.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_404_NOT_FOUND)

    def test_updateBlock(self):
        # Tests if you can update a block by ID

        # Creates a new survey and a block
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')

        # Update the block order
        data_block_update = {"title": "block number one!", "order": 200}
        response_3 = self.client.patch(f"/api/blocks/{response_2.json()['id']}", data_block_update, format='json')
        expected = {"id": response_3.json()['id'],"title": "block number one!", "order": 200, "survey": response_3.json()['survey'], "description": ''}
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)
        self.assertEqual(response_3.json(), expected)
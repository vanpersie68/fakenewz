import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import surveybuilder.models
import requests
from django.contrib.auth.models import User


class SurveyTestCase(APITestCase):
    # Testing suite for all functions related to the entity Survey
    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_retrieve_survey(self):
        survey_data  = { 
            'name': 'test survey 1',
            'language': 'English',
            "time_limit_minutes": 60,
            "status": 1,
            "researcher":2000
        }

        # send a post request to create the survey
        response = self.client.post('/api/surveys/', survey_data, format = 'json')
        # retrieve survey info via get request
        retrieved = self.client.get(f"/api/surveys/{response.json()['id']}")
        print(retrieved.json())

        self.assertEqual(retrieved.json()['name'], 'test survey 1')
        self.assertEqual(retrieved.json()['language'], 'English')
        self.assertEqual(retrieved.json()['time_limit_minutes'], 60)
        self.assertEqual(retrieved.json()['status'], 1)
        self.assertEqual(retrieved.json()['researcher'], 2000)



    def test_create_survey(self):
        survey_data  = { 
            'name': 'test survey 1',
            'language': 'English',
            'consentText': 'qwerty',
            "time_limit_minutes": 60,
            "status": 1,
            "researcher":2000
        }

        # send a post request to create the survey
        oldSurveyCount=surveybuilder.models.Survey.objects.count()
        response = self.client.post('/api/surveys', survey_data, format = 'json')
        # check that the 201 created code is sent back
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check that the survey is added to the database
        self.assertEqual(surveybuilder.models.Survey.objects.count(), oldSurveyCount+1)
        
        retrieved = surveybuilder.models.Survey.objects.get(pk=response.json()['id'])
        self.assertEqual(retrieved.name,'test survey 1')
        self.assertEqual(retrieved.language,'English')
        self.assertEqual(retrieved.consentText,'qwerty')
        self.assertEqual(retrieved.time_limit_minutes, 60)
        self.assertEqual(retrieved.status, 1)

    
    # tests that non-existent survey URLs returns 404 code
    def test_nonexistent_survey(self):
        response = self.client.get('/api/surveys/100')
        # as we haven't created a survey with this id, this should return a 404 error
        self.assertEqual(response.status_code, 404)
        # check the error message given matches what we expect
        expected_message = {'Message': 'The survey can\'t be found.'}
        self.assertEqual(response.json(), expected_message)

    def test_nonexistent_survey_blocks(self):
        response = self.client.get('/api/surveys/100/blocks')
        # as we haven't created a survey with this id, this should return a 404 error
        self.assertEqual(response.status_code, 404)
        # check the error message given matches what we expect
        expected_message = {'Message': 'The survey can\'t be found.'}
        self.assertEqual(response.json(), expected_message)

    def test_nonexistent_survey_data(self):
        response = self.client.get('/api/surveys/100/data')
        # as we haven't created a survey with this id, this should return a 404 error
        self.assertEqual(response.status_code, 404)
        # check the error message given matches what we expect
        expected_message = {'Message': 'The survey can\'t be found.'}
        self.assertEqual(response.json(), expected_message)
    
    def test_listSurveys(self):
        # Tests whether a list of all surveys created by the researcher can be retrieved
        survey_data = {
            'name': 'test survey 1',
            'language': 'English',
            'consentText': 'qwerty',
            "time_limit_minutes": 60,
            "status": 1,
            "researcher": 2000
        }
        survey_data2 = {
            'name': 'test survey 2',
            'language': 'English',
            "time_limit_minutes": 120,
            "status": 0,
            "researcher": 2000
        }
        # send a post request to create the survey
        response = self.client.post('/api/surveys', survey_data, format='json')
        # check that the 201 created code is sent back
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # send another post request to create the survey
        response = self.client.post('/api/surveys', survey_data2, format='json')
        # check that the 201 created code is sent back
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/surveys/researcher/2000")
        # check whether there are two survey
        self.assertGreaterEqual(len(response.json()), 2)

    def test_addSurvey(self):
        # Tests that a survey can be created

        data = {"name": "Survey One!", "language": "French", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        response = self.client.post("/api/surveys", data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.json()), 16)

        # Check that the database has greater than 0 surveys.
        response_2 = self.client.get("/api/surveys")
        self.assertGreater(len(response_2.json()), 0)
    
    def test_getIDsurvey(self):
        # Tests fetching a specific survey by ID

        # Creates a new survey
        data = {"name": "Survey Two!", "language": "English", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        response = self.client.post("/api/surveys", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Fetchs the survey by ID
        response_2 = self.client.get(f"/api/surveys/{response.json()['id']}")
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

    def test_modifySurvey(self):
        # Tests patching a survey by ID

        # Creates a new survey
        data = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        response = self.client.post("/api/surveys", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Modifies the survey by changing the language to Turkish
        response_2 = self.client.patch(f"/api/surveys/{response.json()['id']}", {'language': 'Turkish'}, format='json')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)

        # Confirms the survey has been changed
        response_3 = self.client.get(f"/api/surveys/{response_2.json()['id']}")
        self.assertEqual(response_3.status_code, status.HTTP_200_OK)

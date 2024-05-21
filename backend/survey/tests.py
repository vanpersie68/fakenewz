import json
import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from surveybuilder.models import Survey, Block
from rest_framework.authtoken.admin import User
from rest_framework import status
from rest_framework.test import APITestCase

import surveybuilder


class ClinicTestCase(APITestCase):

    def setUp(self):
        user=User.objects.create(id=3000, username="testUser")
        survey=Survey.objects.create(id=2000,researcher=user)
        Block.objects.create(id=2000,survey=survey,order=1)

    def export(self):
        survey_data = {
            'name': 'test survey 1',
            'language': 'English',
            'consentText': 'qwerty',
            "time_limit_minutes": 60,
            "status": 1,
            "researcher": 3000
        }

        # send a post request to create the survey
        oldSurveyCount = surveybuilder.models.Survey.objects.count()
        response = self.client.post('/api/surveys', survey_data, format='json')
        # check that the 201 created code is sent back
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # check that the survey is added to the database
        self.assertEqual(surveybuilder.models.Survey.objects.count(), oldSurveyCount + 1)

        retrieved = self.client.get(f"/survey/exportSurvey/{response.json()['id']}")
        # check whether the retrieved content is the same as expected
        self.assertEqual(retrieved.json()['name'], 'test survey 1')
        self.assertEqual(retrieved.json()['language'], 'English')
        self.assertEqual(retrieved.json()['time_limit_minutes'], 60)
        self.assertEqual(retrieved.json()['status'], 1)
        self.assertEqual(retrieved.json()['researcher'], 3000)
        self.assertEqual(retrieved.json()['blocks'], [])
        self.assertEqual(retrieved.json()['randomSections'], [])

        
    def import_survey(self):
        survey_json='''
        {"id": 4, "researcher": 3000, "name": "Survey Title", "language": "English", "consentText": "qwerty", "time_limit_minutes": 60, "status": 1, "current_submission": 0, "required_submission": 0, "create_time": "2022-04-12T02:39:50.870112Z", "publish_time": "2022-04-12T02:42:10.475000Z", "expire_time": null, "is_repeat_answer": true, "code": "2sj36RPN", "blocks": [{"id": 8, "survey": 4, "title": "Default Block Title", "description": "", "order": 1, "questions": [{"id": 9, "block": 8, "name": "text entry1", "type": "Text entry", "description": "", "required": false, "order": 1, "typedata": {"id": 4, "question": 9, "query": "", "textboxMax": 10, "textboxMin": 0, "validate": true, "ansType": "Text"}}]}, {"id": 9, "survey": 4, "title": "Default Block Title", "description": "", "order": 2, "questions": [{"id": 10, "block": 9, "name": "number scale 1", "type": "Number scale", "description": "", "required": false, "order": 1, "typedata": {"id": 4, "question": 10, "minTitle": "", "middleTitle": "", "maxTitle": "", "interval": 1, "numberMax": 6, "numberMin": 0, "minTitleOn": true, "midTitleOn": true, "maxTitleOn": true}}]}, {"id": 10, "survey": 4, "title": "Default Block Title", "description": "", "order": 3, "questions": [{"id": 11, "block": 10, "name": "multiple choice1", "type": "Multiple choice", "description": "", "required": false, "order": 1, "typedata": {"id": 2, "question": 11, "options": 3, "isDropDown": false, "isCheckbox": false, "textboxMax": 1, "textboxMin": 1, "multipleAnswers": false}, "choices": [{"id": 4, "question": 2, "order": 1, "title": "choice1"}, {"id": 5, "question": 2, "order": 2, "title": "choice2"}, {"id": 6, "question": 2, "order": 3, "title": "choice3"}]}, {"id": 12, "block": 10, "name": "button row1", "type": "Button row", "description": "", "required": false, "order": 2, "typedata": {"id": 2, "question": 12, "numberButtons": 2}, "buttons": [{"id": 3, "buttonRow": 2, "buttonText": "button 1", "buttonType": "", "buttonIcon": "", "answered": false, "jumpBlockId": 0}, {"id": 4, "buttonRow": 2, "buttonText": "button 2", "buttonType": "", "buttonIcon": "", "answered": false, "jumpBlockId": 0}]}]}], "randomSections": [{"survey": 4, "display": 1, "startWith": 1, "endWith": 1, "index": 0}, {"survey": 4, "display": 1, "startWith": 2, "endWith": 2, "index": 1}, {"survey": 4, "display": 1, "startWith": 3, "endWith": 3, "index": 2}]}
        '''
        oldSurveyCount = surveybuilder.models.Survey.objects.count()
        response = self.client.post(f"/survey/import/3000",json.loads(survey_json), format='json')
        # check whether the survey import is successful
        self.assertEqual('success',response.json()['status'])
        # check that the survey is added to the database
        self.assertEqual(surveybuilder.models.Survey.objects.count(), oldSurveyCount + 1)


    def export_response_csv(self):
        data_survey_response = {
            "survey_id": 2000,
            "contact_info": "123@qq.com",
            "response_blocks": [
                {
                    "block_id": 2000,
                    "response_questions": [
                        {
                            "question_id": 2000,
                            "response_question_answer": [
                                {
                                    "title": "how old are you",
                                    "answerText": None,
                                    "answerDecimal": 18
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data_survey_response2 = {
            "survey_id": 2000,
            "contact_info": "123@qq.com",
            "response_blocks": [
                {
                    "block_id": 2000,
                    "response_questions": [
                        {
                            "question_id": 2000,
                            "response_question_answer": [
                                {
                                    "title": "Where are you from?",
                                    "answerText": "China",
                                    "answerDecimal": 0
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get("/survey/exportCsv/2000")
        # check that the response csv function works correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)





import os, django
import random
import string

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class SaveResponseTestCase(APITestCase):

    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_save_response(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey, format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)
        ran_code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "uuid": ran_code,
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": ran_code,
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "response_question_answer": [
                                {
                                    "title": "how old are you",
                                    "answerText": None,
                                    "answerDecimal": 18,
                                    "uuid": ran_code,
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_survey_not_exist(self):
    #     # Create a new survey
    #     data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
    #                    "time_limit_minutes": 60, "status": 1, "researcher": 2000}
    #     survey_response = self.client.post("/api/surveys", data_survey, format='json')
    #     self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Create a new block
    #     data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
    #     block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
    #                                       format='json')
    #     self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Creates a new question
    #     data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
    #     question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
    #                                          format='json')
    #     self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Publish the survey
    #     data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
    #                            "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
    #     publish_response = self.client.patch(f"/api/surveys/{block_response.json()['id']}", data_publish_survey,
    #                                          format='json')
    #     self.assertEqual(publish_response.status_code, status.HTTP_200_OK)
    #     data_survey_response = {
    #         "survey_id": survey_response.json()['id'] + 1,
    #         "create_datatime": "2022-03-23T14:36:36.045234Z",
    #         "end_datatime": "2022-03-23T14:36:36.045234Z",
    #         "contact_info": "123@qq.com",
    #         "response_blocks": [
    #             {
    #                 "block_id": 1,
    #                 "response_questions": [
    #                     {
    #                         "question_id": 1,
    #                         "response_question_answer": [
    #                             {
    #                                 "title": "how old are you",
    #                                 "answerText": None,
    #                                 "answerDecimal": 18
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     survey_response1 = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
    #     self.assertEqual(survey_response1.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertEqual(survey_response1.json()['Message'], 'The survey can\'t be found.')
    #
    # def test_survey_is_full(self):
    #     # Create a new survey
    #     data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
    #                    "time_limit_minutes": 60, "status": 1, "researcher": 2000}
    #     survey_response = self.client.post("/api/surveys", data_survey, format='json')
    #     self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Create a new block
    #     data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
    #     block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
    #                                       format='json')
    #     self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Creates a new question
    #     data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
    #     question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
    #                                          format='json')
    #     self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)
    #
    #     # Publish the survey
    #     data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
    #                            "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
    #     publish_response = self.client.patch(f"/api/surveys/{block_response.json()['id']}", data_publish_survey,
    #                                          format='json')
    #     self.assertEqual(publish_response.status_code, status.HTTP_200_OK)
    #
    #     data_survey_response = {
    #         "survey_id": survey_response.json()['id'],
    #         "create_datatime": "2022-03-23T14:36:36.045234Z",
    #         "end_datatime": "2022-03-23T14:36:36.045234Z",
    #         "contact_info": "123@qq.com",
    #         "response_blocks": [
    #             {
    #                 "block_id": block_response.json()['id'],
    #                 "response_questions": [
    #                     {
    #                         "question_id": question_response.json()['id'],
    #                         "response_question_answer": [
    #                             {
    #                                 "title": "how old are you",
    #                                 "answerText": None,
    #                                 "answerDecimal": 18
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     survey_response1 = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
    #     survey_response2 = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
    #     survey_response3 = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
    #     self.assertEqual(survey_response1.status_code, status.HTTP_200_OK)
    #     self.assertEqual(survey_response1.json()['Message'], 'success')
    #     self.assertEqual(survey_response2.status_code, status.HTTP_200_OK)
    #     self.assertEqual(survey_response2.json()['Message'], 'The survey is full, survey is now closed')
    #     self.assertEqual(survey_response3.status_code, status.HTTP_200_OK)
    #     self.assertEqual(survey_response3.json()['Message'], 'The survey has already full.')

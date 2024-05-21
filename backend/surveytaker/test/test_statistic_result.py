import django
import os

from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APITestCase
from rest_framework import status


class StatisticResultTestCase(APITestCase):

    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_text_entry(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block1
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question1
        data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "uuid": "123",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "how old are you",
                                    "answerText": None,
                                    "uuid": "123",
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

        response = self.client.get(f"/api/st/survey/result/0/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'Text entry')
        self.assertEqual(len(response.json()), 14)

    def test_multiple_choice(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Multiple Choice)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {
            "name": "Default Question Title",
            "type": "Multiple choice",
            "description": "",
            "required": 0,
            "order": 1
        }
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_choice1 = {"order": "1", "title": "choice1"}
        data_choice2 = {"order": "2", "title": "choice2"}
        data_choice3 = {"order": "3", "title": "choice3"}
        self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice1,
                         format='json')
        self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice2,
                         format='json')
        self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice3,
                         format='json')

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "uuid": "123",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "choice1",
                                    "answerText": "selected",
                                    "uuid": "123",
                                    "answerDecimal": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/st/survey/result/0/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'Multiple choice')
        self.assertEqual(len(response.json()), 14)

    def test_number_scale(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Number Scale)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Number scale", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_max_value = {"numberMax": 5}
        self.client.post(f"/api/questions/inner/{question_response.json()['id']}", data_max_value,
                         format='json')

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "uuid": "123",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "Default Question Title",
                                    "uuid": "123",
                                    "answerText": "4",
                                    "answerDecimal": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/st/survey/result/0/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'Number scale')
        self.assertEqual(len(response.json()), 14)

    def test_button_row(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Button row)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {
            "name": "Default Question Title",
            "type": "Button row",
            "description": "",
            "required": 0,
            "order": 1
        }
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_button1 = {"buttonText": "Default"}
        data_button1_title = {"id": 1, "buttonText": "b1", "jumpBlockId": 0}
        data_button2 = {"buttonText": "Default"}
        data_button2_title = {"id": 2, "buttonText": "b2", "jumpBlockId": 0}
        data_button3 = {"buttonText": "Default"}
        data_button3_title = {"id": 3, "buttonText": "b3", "jumpBlockId": 0}
        self.client.post(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button1,
                         format='json')
        self.client.post(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button2,
                         format='json')
        self.client.post(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button3,
                         format='json')
        self.client.patch(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button1_title,
                          format='json')
        self.client.patch(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button2_title,
                          format='json')
        self.client.patch(f"/api/questions/buttonrow/{question_response.json()['id']}", data_button3_title,
                          format='json')

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "uuid": "123",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "b1",
                                    "answerText": "selected",
                                    "uuid": "123",
                                    "answerDecimal": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/st/survey/result/0/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'Button row')
        self.assertEqual(len(response.json()), 14)

    def test_news_post(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(News post)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "News post", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_article = {
            "articleImageLink": "https://m.files.bbci.co.uk/modules/bbc-morph-news-waf-page-meta/5.2.0/bbc_news_logo"
                                ".png",
            "articleURL": "https://www.bbc.com/news/live/world-europe-61157670", "articleSource": "www.bbc.com",
            "articleTitle": "Ukraine war latest news: Russia gives fresh ultimatum to fighters in Mariupol - BBC News",
            "articleSnippet": "Russia gives a new deadline on Wednesday to Ukrainian troops in the port city of "
                              "Mariupol to surrender.",
            "articleStyle": "Twitter"}
        self.client.patch(f"/api/questions/inner/{question_response.json()['id']}", data_article,
                          format='json')

        data_like = {"articleLikesOn": 1, "articleLikes": "1"}
        data_comment = {"articleCommentsOn": 1, 'articleComments': "1"}
        data_share = {"articleSharesOn": 1, "articleShares": "1"}

        self.client.patch(f"/api/questions/inner/{question_response.json()['id']}", data_like,
                          format='json')
        self.client.patch(f"/api/questions/inner/{question_response.json()['id']}", data_comment,
                          format='json')
        self.client.patch(f"/api/questions/inner/{question_response.json()['id']}", data_share,
                          format='json')

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "uuid": "123",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "Like",
                                    "answerText": "selected",
                                    "uuid": "123",
                                    "answerDecimal": None
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        response = self.client.post("/api/st/survey/saveResponse", data_survey_response, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"/api/st/survey/result/0/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'News post')
        self.assertEqual(len(response.json()), 14)

    def test_is_preview(self):
        # Create a new survey
        data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                       "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block1
        data_block = {"order": 1, "survey": survey_response.json()['id'], "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question1
        data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        # Publish the survey
        data_publish_survey = {"status": 1, "publish_time": "2022-03-25T13:10:45.878Z", "is_repeat_answer": 1,
                               "expire_time": "2022-09-25T13:10:45.878Z", "required_submission": "2"}
        publish_response = self.client.patch(f"/api/surveys/{survey_response.json()['id']}", data_publish_survey,
                                             format='json')
        self.assertEqual(publish_response.status_code, status.HTTP_200_OK)

        data_survey_response = {
            "survey_id": survey_response.json()['id'],
            "create_datatime": "2022-03-23T14:36:36.045234Z",
            "end_datatime": "2022-03-23T14:36:36.045234Z",
            "contact_info": "123@qq.com",
            "uuid": "123",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/100.0.4896.88 Safari/537.36",
            "preview": 1,
            "response_blocks": [
                {
                    "block_id": block_response.json()['id'],
                    "uuid": "123",
                    "response_questions": [
                        {
                            "question_id": question_response.json()['id'],
                            "uuid": "123",
                            "response_question_answer": [
                                {
                                    "title": "how old are you",
                                    "uuid": "123",
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

        response = self.client.get(f"/api/st/survey/result/1/{survey_response.json()['id']}")
        self.assertEqual(response.json()['blocks'][0]['questions'][0]['type'], 'Text entry')
        self.assertEqual(len(response.json()), 14)

    def test_not_exist(self):
        response = self.client.get(f"/api/st/survey/result/0/10")
        self.assertEqual(response.json()['Message'], 'The survey can\'t be found.')

        response = self.client.get(f"/api/st/survey/result/0/1")
        self.assertEqual(response.json()['Message'], 'The survey can\'t be found.')

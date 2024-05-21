import os, django

from django.contrib.auth.models import User

os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status


class MultipleChoiceTestCase(APITestCase):

    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_add_choice(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_choice = {"order": "1", "title": "Default"}
        choice_response = self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice,
                                           format='json')
        self.assertEqual(choice_response.status_code, status.HTTP_201_CREATED)

    def test_patch_choice(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_choice = {"order": "1", "title": "Default"}
        choice_response = self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice,
                                           format='json')

        id = choice_response.json()['id']
        data_patch = {"id": id, "title": "abc"}
        patch_response = self.client.patch(f"/api/questions/multi/{question_response.json()['id']}", data_patch,
                                            format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

    def test_delete_choice(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        data_choice = {"order": "1", "title": "Default"}
        choice_response = self.client.post(f"/api/questions/multi/{question_response.json()['id']}", data_choice,
                                           format='json')
        self.assertEqual(choice_response.status_code, status.HTTP_201_CREATED)
        id = choice_response.json()['id']
        data_delete = {"id": id}
        delete_response = self.client.delete(f"/api/questions/multi/{question_response.json()['id']}", data_delete,
                                             format='json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_multiple_choice_question(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')
        self.assertEqual(survey_response.status_code, status.HTTP_201_CREATED)

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')
        self.assertEqual(block_response.status_code, status.HTTP_201_CREATED)

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')
        self.assertEqual(question_response.status_code, status.HTTP_201_CREATED)

        # Check the type of question is Text Entry
        self.assertEqual(question_response.json()['type'], 'Multiple choice')

        # Check the text entry question has been added to database
        get_response = self.client.get(f"/api/questions/multi/{question_response.json()['id']}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')

        # get question's information
        get_response = self.client.get(f"/api/questions/multi/{question_response.json()['id']}")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_response.json()), 10)
        self.client.delete(f"/api/surveys/{survey_response.json()['id']}")

    def test_patch_validate(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')

        # update multipleAnswers state to true
        data_patch_true = {'multipleAnswers': 1}
        patch_response = self.client.patch(f"/api/questions/multiChoice/{question_response.json()['id']}",
                                           data_patch_true,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['multipleAnswers'], 1)

        # update multipleAnswers state to false
        data_patch_false = {'multipleAnswers': 0}
        patch_response = self.client.patch(f"/api/questions/multiChoice/{question_response.json()['id']}",
                                           data_patch_false,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['multipleAnswers'], 0)
        self.client.delete(f"/api/surveys/{survey_response.json()['id']}")

    def test_patch_answers(self):
        # Create a new survey
        data_survey = data_survey = {"name": "Unit Test(Text Entry)", "language": "English", "consentText": "qwerty",
                                     "time_limit_minutes": 60, "status": 1, "researcher": 2000}
        survey_response = self.client.post("/api/surveys", data_survey, format='json')

        # Create a new block
        data_block = {"order": 1, "survey": 3, "title": "Unit Test(Text Entry)"}
        block_response = self.client.post(f"/api/surveys/{survey_response.json()['id']}/blocks", data_block,
                                          format='json')

        # Creates a new question
        data_question = {"type": "Multiple choice", "name": "Default Question Title", "required": 0, "order": 1}
        question_response = self.client.post(f"/api/blocks/{block_response.json()['id']}/questions", data_question,
                                             format='json')

        # update minimum input length
        data_patch_min = {'textboxMin': 1}
        patch_response = self.client.patch(f"/api/questions/multiChoice/{question_response.json()['id']}",
                                           data_patch_min,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['textboxMin'], 1)

        # update maximum input length
        data_patch_max = {'textboxMax': 2}
        patch_response = self.client.patch(f"/api/questions/multiChoice/{question_response.json()['id']}",
                                           data_patch_max,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['textboxMax'], 2)
        self.client.delete(f"/api/surveys/{survey_response.json()['id']}")

    def test_exception(self):
        # try to get question information which is not exist
        get_response = self.client.get(f"/api/questions/multi/10")
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

        patch_response = self.client.patch(f"/api/questions/multiChoice/10")
        self.assertEqual(patch_response.status_code, status.HTTP_404_NOT_FOUND)

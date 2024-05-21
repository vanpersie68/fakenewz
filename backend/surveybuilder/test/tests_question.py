import os,django
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_core.settings'
django.setup()
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import requests
from django.contrib.auth.models import User


class QuestionTestCase(APITestCase):
    # Testing suite for all functions related to the Question entity

    ########## General Question Testing ##########
    def setUp(self):
        User.objects.create(id=2000, username="testUser")

    def test_addQuestion(self):
        # Testing if you can add a question to a block

        # Creates a new survey and a block
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')

        # Creates a question in the new block
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1, "description": "empty"}
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_3.json()), 8)

        # Check the question has been added to the block
        response_4 = self.client.get(f"/api/blocks/{response_2.json()['id']}/questions")
        self.assertGreater(len(response_4.json()), 0)

    def test_fetchQuestion(self):
        # Tests if you can fetch a question by ID

        # Creates a new survey, a block, and a question
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        # Finds the question by it's ID
        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()), 8)

    def test_patchQuestion(self):
        # Tests if you can modify a question by ID

        # Creates a new survey, a block, and a question
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        # Modifies the question by changing required to 0
        response_4 = self.client.patch(f"/api/questions/{response_3.json()['id']}", {'required': 0}, format='json')
        expected = {"name": "First Question!", "type": "News post", "required": 0, "order": 1, "description": "empty", "block": response_3.json()['block'],'image': '', "id": response_3.json()['id']}
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(response_4.json(), expected)

    def test_deleteQuestion(self):
        # Tests if you can delete a question by ID

        # Creates a new survey, a block, and a question
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        # Deletes the question
        response_4 = self.client.delete(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the question doesn't exist
        response_5 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_5.status_code, status.HTTP_404_NOT_FOUND)

    ########## Social Media Question Testing ##########   

    def test_emptySocialMediaQuestionMade(self):
        # Tests that an empty social media question is generated when passed the 'socialmedia' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 15)


    def add_postAddonField_data(self):
        # test to add a post addon field data
        # create question first
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1,
                         "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        qid = response_3.json()['id']
        # test post
        addon_data = {"title": "test title", "count": 123, "icon": "like.jpg"}
        response_4 = self.client.post(f"/api/questions/postaddonfield/{qid}", addon_data, format="json")
        self.assertEqual(response_4.status_code, status.HTTP_201_CREATED)


    def edit_postAddonField_data(self):
        # test to edit a post addon field data
        # create question first
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1,
                         "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        qid = response_3.json()['id']
        # add post addon field
        addon_data = {'title': 'test title', 'count': 123, 'icon': 'like.jpg'}
        response_4 = self.client.post(f"/api/questions/postaddonfield/{qid}", addon_data, format="json")

        # test edit
        edit_data = {"id": response_4.json()['id'], "title": "test edit", "count": 321, "icon": "hate.jpg"}
        response_5 = self.client.patch(f"/api/questions/postaddonfield/{qid}", edit_data, format="json")
        edit_data['postRow'] = response_3.json()['id']
        self.assertEqual(response_5.status_code, status.HTTP_200_OK)
        self.assertEqual(response_5.json(), edit_data)


    def get_postAddonField_data(self):
        # test to get a post addon field data
        # create question first
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1,
                         "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        qid = response_3.json()['id']
        # add post addon field
        addon_data = {'title': 'test title', 'count': 123, 'icon': 'like.jpg'}
        response_4 = self.client.post(f"/api/questions/postaddonfield/{qid}", addon_data, format="json")
        # test get
        response_5 = self.client.get(f"/api/questions/postaddonfield/{qid}", format="json")
        get_data = {"id": response_4.json()['id'], "postRow": qid, "title": "test title", "count": 123, "icon": "like.jpg"}
        self.assertEqual(response_5.status_code, status.HTTP_200_OK)
        self.assertEqual(response_5.json()['addon'], [get_data])

    def del_postAddonField_data(self):
        # test to del a post addon field data
        # create question first
        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "News post", "required": 1, "order": 1,
                         "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        qid = response_3.json()['id']
        # add post addon field
        addon_data = {'title': 'test title', 'count': 123, 'icon': 'like.jpg'}
        response_4 = self.client.post(f"/api/questions/postaddonfield/{qid}", addon_data, format="json")
        addon_id = response_4.json()['id']
        # test del
        response_5 = self.client.delete(f"/api/questions/postaddonfield/{qid}", {'id': addon_id}, format="json")
        self.assertEqual(response_5.status_code, status.HTTP_204_NO_CONTENT)



    ########## Button Row Question Testing ##########

    def test_emptyButtonRowQuestionMade(self):
        # Tests that an empty button row question is generated when passed the 'buttonrow' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "Button row", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 3)

    def test_modifyingButtonsInButtonQuestion(self):
        # Tests that you can remove, add, query, and delete button questions (should probably be seperate tests)

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "Button row", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        # query the question to find the buttonrow ID
        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)

        # query the ID of the buttonrow type and check there are no buttons
        response_5 = self.client.get(f"/api/questions/buttonrow/{response_4.json()['type']['id']}")
        self.assertEqual(response_5.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_5.json()), 4)
        self.assertEqual(len(response_5.json()['buttons']), 0)

        # add a button the buttonrow question
        data_button = {"buttonText": "Button Text", "buttonType": "Button Type", "buttonIcon": "Button Icon", "answered": 1}
        response_6 = self.client.post(f"/api/questions/buttonrow/{response_4.json()['type']['id']}", data_button, format='json')
        expected_button = {"id": response_6.json()['id'], "buttonRow": response_4.json()['type']['id'], "buttonText": "Button Text", "buttonType": "Button Type", "buttonIcon": "Button Icon", "answered": True,"jumpBlockId": 0}
        self.assertEqual(response_6.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_6.json()), 7)
        self.assertEqual(response_6.json(), expected_button)

        # query the ID of the buttonrow type and check there is one buton
        response_7 = self.client.get(f"/api/questions/buttonrow/{response_4.json()['type']['id']}")
        self.assertEqual(response_7.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_7.json()['buttons']), 1)

        # patch the button using the buttonrow ID
        data_buttonpatch = {"id": response_6.json()['id'], "buttonText": "New button text", "buttonType": "New button type", "buttonIcon": "Button Icon", "answered": "1"}
        expected_buttonpatch = {"id": response_6.json()['id'], "buttonRow": response_4.json()['type']['id'], "buttonText": "New button text", "buttonType": "New button type", "buttonIcon": "Button Icon", "answered": True,"jumpBlockId": 0}
        response_8 = self.client.patch(f"/api/questions/buttonrow/{response_4.json()['type']['id']}", data_buttonpatch, format='json')
        self.assertEqual(response_8.status_code, status.HTTP_200_OK)
        self.assertEqual(response_8.json(), expected_buttonpatch)

        # delete the one button that exists
        data_buttonid = {"id": response_6.json()['id']}
        response_9 = self.client.delete(f"/api/questions/buttonrow/{response_4.json()['type']['id']}", data_buttonid, format='json')
        self.assertEqual(response_9.status_code, status.HTTP_204_NO_CONTENT)
        response_10 = self.client.get(f"/api/questions/buttonrow/{response_4.json()['type']['id']}")
        self.assertEqual(response_10.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_10.json()['buttons']), 0)

    ########## Text Box Question Testing ##########

    def test_emptyTextboxNumberQuestionMade(self):
        # Tests that an empty textbox number question is generated when passed the 'textbox_number' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 7)
        data_patch_integer = {'ansType': 'Integer'}
        patch_response = self.client.patch(f"/api/questions/textentry/{response_4.json()['id']}",
                                           data_patch_integer,
                                           format='json')
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.json()['ansType'], 'Integer')

    def test_emptyTextboxTextQuestionMade(self):
        # Tests that an empty textbox text question is generated when passed the 'textbox_text' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"type": "Text entry", "name": "Default Question Title", "required": 0, "order": 1}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')
        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 7)

    ########## Multiple Choice Question Testing ##########

    def test_emptyMultiChoiceQuestionMade(self):
        # Tests that an empty multiple choice question is generated when passed the 'multiplechoice' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "Multiple choice", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 9)

    def test_modifyingChoicesInMultiChoiceQuestion(self):
        # Tests that you can remove, add, query, and delete choices in multiple choice (should probably be seperate tests)

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "Multiple choice", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        # query the question to find the multiplechoice question ID
        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)

        # query the ID of the multichoice question type and check there are no choices
        response_5 = self.client.get(f"/api/questions/multi/{response_4.json()['type']['id']}")
        self.assertEqual(response_5.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_5.json()), 10)
        self.assertEqual(len(response_5.json()['choices']), 0)

        # add a choice the multiple choice question
        data_choice = {"order": "1", "title": "Title!"}
        response_6 = self.client.post(f"/api/questions/multi/{response_4.json()['type']['id']}", data_choice, format='json')
        expected_choice = {"id": response_6.json()['id'], "question": response_4.json()['type']['id'], "order": 1, "title": "Title!"}
        self.assertEqual(response_6.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response_6.json()), 4)
        self.assertEqual(response_6.json(), expected_choice)

        # query the ID of the multiplechoice question and check there is one choice
        response_7 = self.client.get(f"/api/questions/multi/{response_4.json()['type']['id']}")
        self.assertEqual(response_7.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_7.json()['choices']), 1)

        # patch the choice using the choice ID
        data_choicepatch = {"id": response_7.json()['choices'][0]['id'], "title": "New Title"}
        expected_choicepatch = {"id": response_6.json()['id'], "question": response_4.json()['type']['id'], "order": 1, "title": "New Title"}
        response_8 = self.client.patch(f"/api/questions/multi/{response_4.json()['type']['id']}", data_choicepatch, format='json')
        self.assertEqual(response_8.status_code, status.HTTP_200_OK)
        self.assertEqual(response_8.json(), expected_choicepatch)

        # delete the one button that exists
        data_choiceid = {"id": response_7.json()['choices'][0]['id']}
        response_9 = self.client.delete(f"/api/questions/multi/{response_4.json()['type']['id']}", data_choiceid, format='json')
        self.assertEqual(response_9.status_code, status.HTTP_204_NO_CONTENT)
        response_10 = self.client.get(f"/api/questions/multi/{response_4.json()['type']['id']}")
        self.assertEqual(response_10.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_10.json()['choices']), 0)

    ########## Number Scale Question Testing ##########

    def test_emptyNumberScaleQuestionMade(self):
        # Tests that an empty number scale question is generated when passed the 'numberscale' type

        data_survey = {"name": "Survey Three!", "language": "Japanese", "consentText": "empty", "time_limit_minutes": 60, "status": 1,"researcher":2000}
        data_block = {"title": "block number one!", "order": 1}
        data_question = {"name": "First Question!", "type": "Number scale", "required": 1, "order": 1, "description": "empty"}
        response = self.client.post("/api/surveys", data_survey, format='json')
        response_2 = self.client.post(f"/api/surveys/{response.json()['id']}/blocks", data_block, format='json')
        response_3 = self.client.post(f"/api/blocks/{response_2.json()['id']}/questions", data_question, format='json')

        response_4 = self.client.get(f"/api/questions/{response_3.json()['id']}")
        self.assertEqual(response_4.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_4.json()['type']), 11)


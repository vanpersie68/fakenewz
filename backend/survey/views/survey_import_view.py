from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import NotAcceptable
from rest_framework.response import Response
import json
from google.cloud import translate_v2 as translate
from google.oauth2.service_account import Credentials

# from django.conf import settings
# BASE_DIR = settings.BASE_DIR
# ? how to join base dir with the json file in docker container
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './secret_key/fine-slice-382222-c97b24e88c19.json'
# * Currently hard code the path
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/CS74-1-2023S1/backend/secret_key/fine-slice-382222-c97b24e88c19.json'

from surveybuilder.const import questionTypeModel
from surveybuilder.models import Survey, Question, Block, MultiChoice, ButtonQuestion, RandomSections, PostAddonfield, \
    MatrixTable, RankOrder, Sliders, Groups


@swagger_auto_schema(
    request_body=openapi.Schema(
        title="Survey configuration",
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'language': openapi.Schema(type=openapi.TYPE_STRING),
            'blocks': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT)),
            'randomSections': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
        }),
    operation_summary='import survey according to survey configuration file', methods=['POST'])
@api_view(["POST"])
def import_survey(request, researcher_id):
    """
    post:
    Import survey according to survey configuration file
     """
    try:
        import_survey_data(request.data, researcher_id)
        return Response({"status": "success"})
    except Exception as e:
        raise NotAcceptable(detail="Survey cannot be imported!")


def import_survey_data(data, researcher_id, to_language):
    survey = Survey()
    researcher = User.objects.get(id=researcher_id)
    survey.researcher = researcher
    lib_langage = {"en": "English",
                   "ka": "ಕನ್ನಡ ",
                   "ja": "日本語",
                   "ur": "اردو",
                   "hi": "हिन्दी",
                   "zh": "中文"
                   }
    if 'name' in data and to_language is not None:
        survey.name = translate_survey_data(data['name'], to_language)
        print("Translator is apply on:" + survey.name)
    else:
        survey.name = data['name']
    if 'language' in data and to_language is not None:
        survey.language = lib_langage[to_language]
    else:
        survey.language = data['language']

    if 'consentText' in data:
        survey.consentText = data['consentText']
    if 'time_limit_minutes' in data:
        survey.time_limit_minutes = data['time_limit_minutes']
    survey.save()

    if 'blocks' in data:
        for block in data['blocks']:
            b = Block()
            b.survey = survey
            if 'title' in block and to_language is not None:
                # translate title
                b.title = translate_survey_data(block['title'], to_language)
                print("Translator on the title block：" + b.title)
            else:
                b.title = block['title']

            if 'description' in block and to_language is not None:
                # translate description
                b.description = translate_survey_data(block['description'], to_language)
            else:
                b.description = block['description']

            if 'order' in block:
                b.order = block['order']
            b.save()

            if 'questions' in block:
                for question in block['questions']:
                    q = Question()
                    q.block = b
                    if 'name' in question and to_language is not None:
                        q.name = translate_survey_data(question['name'], to_language)
                        print(q.name)
                    else:
                        q.name = question['name']

                    if 'type' in question:
                        q.type = question['type']
                    if 'description' in question:
                        # this part need to check i f need translate
                        q.description = question['description']
                    if 'required' in question:
                        q.required = question['required']
                    if 'order' in question:
                        q.order = question['order']
                    q.save()

                    typedata = question['typedata']
                    datatype = questionTypeModel[q.type]()
                    datatype.question = q
                    if q.type == 'Text entry':
                        if 'query' in typedata and to_language is not None:
                            datatype.query = translate_survey_data(typedata['query'], to_language)
                        else:
                            datatype.query = typedata['query']

                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'validate' in typedata:
                            datatype.validate = typedata['validate']
                        if 'ansType' in typedata:
                            datatype.ansType = typedata['ansType']
                        datatype.save()
                    if q.type == 'Number scale':
                        if 'minTitle' in typedata and to_language is not None:
                            datatype.minTitle = translate_survey_data(typedata['minTitle'], to_language)
                        else:
                            datatype.minTitle = typedata['minTitle']

                        if 'middleTitle' in typedata and to_language is not None:
                            datatype.middleTitle = translate_survey_data(typedata['middleTitle'], to_language)
                        else:
                            datatype.middleTitle = typedata['middleTitle']

                        if 'maxTitle' in typedata and to_language is not None:
                            datatype.maxTitle = translate_survey_data(typedata['maxTitle'], to_language)
                        else:
                            datatype.maxTitle = typedata['maxTitle']

                        if 'interval' in typedata:
                            datatype.interval = typedata['interval']
                        if 'numberMax' in typedata:
                            datatype.numberMax = typedata['numberMax']
                        if 'numberMin' in typedata:
                            datatype.numberMin = typedata['numberMin']
                        if 'minTitleOn' in typedata:
                            datatype.minTitleOn = typedata['minTitleOn']
                        if 'midTitleOn' in typedata:
                            datatype.midTitleOn = typedata['midTitleOn']
                        if 'maxTitleOn' in typedata:
                            datatype.maxTitleOn = typedata['maxTitleOn']
                        datatype.save()
                    if q.type == 'Multiple choice':
                        if 'options' in typedata:
                            datatype.options = typedata['options']
                        if 'isDropDown' in typedata:
                            datatype.isDropDown = typedata['isDropDown']
                        if 'isCheckbox' in typedata:
                            datatype.isCheckbox = typedata['isCheckbox']
                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'multipleAnswers' in typedata:
                            datatype.multipleAnswers = typedata['multipleAnswers']
                        datatype.save()
                        if 'choices' in question:
                            for choice in question['choices']:
                                c = MultiChoice()
                                c.question = datatype
                                if 'order' in choice:
                                    c.order = choice['order']
                                if 'title' in choice and to_language is not None:
                                    c.title = translate_survey_data(choice['title'], to_language)
                                else:
                                    c.title = choice['title']

                                c.save()
                    if q.type == 'Rank order':
                        if 'options' in typedata:
                            datatype.options = typedata['options']
                        if 'isDropDown' in typedata:
                            datatype.isDropDown = typedata['isDropDown']
                        if 'isCheckbox' in typedata:
                            datatype.isCheckbox = typedata['isCheckbox']
                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'multipleAnswers' in typedata:
                            datatype.multipleAnswers = typedata['multipleAnswers']
                        datatype.save()
                        if 'choices' in question:
                            for choice in question['choices']:
                                c = RankOrder()
                                c.question = datatype
                                if 'order' in choice:
                                    c.order = choice['order']
                                if 'title' in choice and to_language is not None:
                                    c.title = translate_survey_data(choice['title'], to_language)
                                else:
                                    c.title = choice['title']
                                c.save()
                    if q.type == 'Matrix table':
                        if 'options' in typedata:
                            datatype.options = typedata['options']
                        if 'isDropDown' in typedata:
                            datatype.isDropDown = typedata['isDropDown']
                        if 'isCheckbox' in typedata:
                            datatype.isCheckbox = typedata['isCheckbox']
                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'multipleAnswers' in typedata:
                            datatype.multipleAnswers = typedata['multipleAnswers']
                        if 'columnConfig' in typedata:
                            datatype.columnConfig = translate_json_data(typedata['columnConfig'],to_language, 'label')
                        if 'tableConfig' in typedata:
                            datatype.tableConfig = translate_json_data(typedata['tableConfig'], to_language, 'name')
                        datatype.save()
                        if 'choices' in question:
                            for choice in question['choices']:
                                c = MatrixTable()
                                c.question = datatype
                                if 'order' in choice:
                                    c.order = choice['order']
                                if 'title' in choice and to_language is not None:
                                    c.title = translate_survey_data(choice['title'], to_language)
                                else:
                                    c.title = choice['title']
                                c.save()
                    if q.type == 'Sliders':
                        if 'options' in typedata:
                            datatype.options = typedata['options']
                        if 'isDropDown' in typedata:
                            datatype.isDropDown = typedata['isDropDown']
                        if 'isCheckbox' in typedata:
                            datatype.isCheckbox = typedata['isCheckbox']
                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'multipleAnswers' in typedata:
                            datatype.multipleAnswers = typedata['multipleAnswers']
                        if 'columnConfig' in typedata:
                            datatype.columnConfig = translate_json_data(typedata['columnConfig'], to_language, 'label')
                        if 'tableConfig' in typedata:
                            datatype.tableConfig = translate_json_data(typedata['tableConfig'], to_language, 'name')
                        if 'min' in typedata:
                            datatype.min = typedata['min']
                        if 'max' in typedata:
                            datatype.max = typedata['max']
                        if 'grid' in typedata:
                            datatype.grid = typedata['grid']
                        datatype.save()
                        if 'choices' in question:
                            for choice in question['choices']:
                                c = Sliders()
                                c.question = datatype
                                if 'order' in choice:
                                    c.order = choice['order']
                                if 'title' in choice and to_language is not None:
                                    c.title = translate_survey_data(choice['title'], to_language)
                                else:
                                    c.title = choice['title']

                                c.save()
                    if q.type == 'Groups':
                        if 'options' in typedata:
                            datatype.options = typedata['options']
                        if 'isDropDown' in typedata:
                            datatype.isDropDown = typedata['isDropDown']
                        if 'isCheckbox' in typedata:
                            datatype.isCheckbox = typedata['isCheckbox']
                        if 'textboxMax' in typedata:
                            datatype.textboxMax = typedata['textboxMax']
                        if 'textboxMin' in typedata:
                            datatype.textboxMin = typedata['textboxMin']
                        if 'multipleAnswers' in typedata:
                            datatype.multipleAnswers = typedata['multipleAnswers']
                        if 'columnConfig' in typedata:
                            datatype.columnConfig = translate_json_data(typedata['columnConfig'], to_language, 'label')
                        if 'tableConfig' in typedata:
                            datatype.tableConfig = translate_json_data(typedata['tableConfig'], to_language, 'name')
                        datatype.save()
                        if 'choices' in question:
                            for choice in question['choices']:
                                c = Groups()
                                c.question = datatype
                                if 'order' in choice:
                                    c.order = choice['order']
                                if 'title' in choice and to_language is not None:
                                    c.title = translate_survey_data(choice['title'], to_language)
                                else:
                                    c.title = choice['title']
                                c.save()
                    if q.type == 'Button row':
                        if 'numberButtons' in typedata:
                            datatype.numberButtons = typedata['numberButtons']
                        datatype.save()
                        if 'buttons' in question:
                            for button in question['buttons']:
                                bt = ButtonQuestion()
                                bt.buttonRow = datatype
                                if 'buttonText' in button and to_language is not None:
                                    bt.buttonText = translate_survey_data(button['buttonText'], to_language)
                                else:
                                    bt.buttonText = button['buttonText']

                                if 'buttonType' in button:
                                    bt.buttonType = button['buttonType']
                                if 'buttonIcon' in button:
                                    bt.buttonIcon = button['buttonIcon']
                                if 'answered' in button:
                                    bt.answered = button['answered']
                                if 'jumpBlockId' in button:
                                    bt.jumpBlockId = button['jumpBlockId']
                                bt.save()
                    if q.type == 'News post':
                        if 'articleURL' in typedata:
                            datatype.articleURL = typedata['articleURL']
                        if 'articleTitle' in typedata:
                            datatype.articleTitle = translate_survey_data(typedata['articleTitle'], to_language)
                        if 'articleSource' in typedata:
                            datatype.articleSource = typedata['articleSource']
                        if 'articleImageLink' in typedata:
                            datatype.articleImageLink = typedata['articleImageLink']
                        if 'articleUser' in typedata:
                            datatype.articleUser = typedata['articleUser']
                        if 'articleStyle' in typedata:
                            datatype.articleStyle = typedata['articleStyle']
                        if 'articleSnippet' in typedata:
                            datatype.articleSnippet = typedata['articleSnippet']
                        if 'articleLikes' in typedata:
                            datatype.articleLikes = typedata['articleLikes']
                        if 'articleComments' in typedata:
                            datatype.articleComments = typedata['articleComments']
                        if 'articleShares' in typedata:
                            datatype.articleShares = typedata['articleShares']
                        if 'articleLikesOn' in typedata:
                            datatype.articleLikesOn = typedata['articleLikesOn']
                        if 'articleCommentsOn' in typedata:
                            datatype.articleCommentsOn = typedata['articleCommentsOn']
                        if 'articleSharesOn' in typedata:
                            datatype.articleSharesOn = typedata['articleSharesOn']
                        if 'numberAddon' in typedata:
                            datatype.numberAddon = typedata['numberAddon']
                        datatype.save()
                        if 'addon' in question:
                            for addon in question['addon']:
                                a = PostAddonfield()
                                a.postRow = datatype
                                if 'title' in addon and to_language is not None:
                                    a.title = translate_survey_data(addon['title'], to_language)
                                else:
                                    a.title = addon['title']
                                if 'icon' in addon:
                                    a.icon = addon['icon']
                                if 'count' in addon:
                                    a.count = addon['count']
                                a.save()

    if 'randomSections' in data:
        for randomSection in data['randomSections']:
            r = RandomSections()
            r.survey = survey
            if 'display' in randomSection:
                r.display = randomSection['display']
            if 'startWith' in randomSection:
                r.startWith = randomSection['startWith']
            if 'endWith' in randomSection:
                r.endWith = randomSection['endWith']
            if 'index' in randomSection:
                r.index = randomSection['index']
            r.save()
    print("Translation clone finished!")


def translate_survey_data(text, to_language):
    creds = Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": "fine-slice-382222",
            "private_key_id": "c97b24e88c19c2cdce1ac8a3dbfb6e58031b2a26",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDP+s2GpClXQJi7\nRZ2nIFTvNW7Y/hfotGoFv/GfKhhDsD/f43zZX9/4OMGlHVwUa4IPYlhEaYhAPxIQ\nY+hWKtCYruzbRJDoaucgZauzjgKeGc6G3qvKoXMOyevbwQGEOUysiyMBFk9+/41S\ntzK63P+tf4QjY/U8Ff4H0nJzaAz18kb8bdrfCDKJKF16lvIKPrlcOkVjno0HzpYi\naBdY7D7GxLKO4Qz4i/uaZP7o/OZWQ7BBJaCRGGprsJSLXjsFyZyNJwsYwL7uLwdo\n9JbYOj99qj1tWxpVn18zXtC2g2JcgEeVg7bhA9cHoyD16951lmT63kelz2g0R5vj\njbC+vX21AgMBAAECggEAEdj7+insQkiQ0sFOniDwKPb05Dop4xZYYtXt7jK2klh1\nosjq1dycY7i7JWg3lqkDKD7QRE6qGplO+4kXTw2tiOy59rcTmF5UJzuSWH4/S0H7\nryc8ps7kCMjbLKiLcMVaBxSJlHZNrCBSCF8gQ1jjuAfRVxgk21snyZQNrkmnkxNn\nuf50raq3bT+29/1zeZLwzTP1GOOzArakT7nkA4hU/sKBMVZFhbVZ92yL5TkLWMFo\naE+jXeWTXE9/O8Qc63uCbqBFfiDVeXEgUlgPErzl3QyClH6/5MU5JCtidtDd9LAq\nN9e6uIMZvHLKyccxAms90L4br5kEFRt1E9DPkaACoQKBgQD5vtu7uDMvfFji28JR\nNkJaARU19yatjNuvtoOTGlglojV4jjyx+iq41Bs7OQsIbtGrCMIL9epgXxMc4b12\n2/9WXyceZN02JWw6nAJprep3rOHPXA1PKMjhBL4VOV/5hMKn8dkS9y6Fb664d725\nsqqHSv1kCvJpJL7Cew4dqUpOuwKBgQDVMC4KNQ/F37HKYi4NY+YNDP/P1yEG4ZCf\nfFyEXJr+PJ3LfTT58piggkJUijZNQM+OEFR7l37S+enHQ4M9FKZRXwmRvLRk/lrv\nmfJ539fyVToQEfi+/3MsjF+cb4NUMoAhpE5kiij4wrf+UO9h3azbUhzF2UieR//T\n+p682b92TwKBgDVYxnkHtK9NAXOb+5r7Wxr8pjo7y+BAeWDEPMC8XN3VE1ToFSDz\nThLjA9oXqjqn6VN+cGy7n8/sHxoJQj5UaetaMfH1G6eIQOEYGA/Y3X+oxydTA2jI\nTnh6WdwQwGZ9LFNRfsvlTuOj4o92zGkROAnkQ9IN4JADEFhcjrxZQA0nAoGBAKnv\n4vNOAsm3m9B43L7dwBbtIsl5ciE7Ev6eslzsOLyqcxovL1iCkjl4PAmJtulz3T8g\nM0flpjnk7v5hCa9Z044PlOAwLRhITRKrg8a0sT3BxCvlN4SAuj1rlBduKKCoNM0c\nXUT1gN1y0hoOSBOaEd0uIjNwFdveBsbiA0EEzgMvAoGAFzeOtTn9KxF+nDCiP1WQ\nzRAREahrUSlaPTDGQQh/Bc4mwzxAo9LV6wAvlILc8bQDAy2gMKayNGsngZNz/x4t\nmUIEhjDuqOxytT1lgrPJ5YcdXCANxTfeKbxqpAY1bE2096M+KRpuPA9vUHXjjZkZ\nhhBxutQbMAeIlXPAAjP3J8U=\n-----END PRIVATE KEY-----\n",
            "client_email": "alex-translator@fine-slice-382222.iam.gserviceaccount.com",
            "client_id": "110800149701420704171",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/alex-translator%40fine-slice-382222.iam.gserviceaccount.com"
        }
    )

    # Instantiates a client
    translate_client = translate.Client(credentials=creds)

    # Translates the text into the target language. translate: max_length=5, 000
    translation = translate_client.translate(
        text,
        target_language=to_language)

    return translation['translatedText']


def translate_json_data(json_dic, to_language, target):
    # translate name and label
    creds = Credentials.from_service_account_info(
        {
            "type": "service_account",
            "project_id": "fine-slice-382222",
            "private_key_id": "c97b24e88c19c2cdce1ac8a3dbfb6e58031b2a26",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDP+s2GpClXQJi7\nRZ2nIFTvNW7Y/hfotGoFv/GfKhhDsD/f43zZX9/4OMGlHVwUa4IPYlhEaYhAPxIQ\nY+hWKtCYruzbRJDoaucgZauzjgKeGc6G3qvKoXMOyevbwQGEOUysiyMBFk9+/41S\ntzK63P+tf4QjY/U8Ff4H0nJzaAz18kb8bdrfCDKJKF16lvIKPrlcOkVjno0HzpYi\naBdY7D7GxLKO4Qz4i/uaZP7o/OZWQ7BBJaCRGGprsJSLXjsFyZyNJwsYwL7uLwdo\n9JbYOj99qj1tWxpVn18zXtC2g2JcgEeVg7bhA9cHoyD16951lmT63kelz2g0R5vj\njbC+vX21AgMBAAECggEAEdj7+insQkiQ0sFOniDwKPb05Dop4xZYYtXt7jK2klh1\nosjq1dycY7i7JWg3lqkDKD7QRE6qGplO+4kXTw2tiOy59rcTmF5UJzuSWH4/S0H7\nryc8ps7kCMjbLKiLcMVaBxSJlHZNrCBSCF8gQ1jjuAfRVxgk21snyZQNrkmnkxNn\nuf50raq3bT+29/1zeZLwzTP1GOOzArakT7nkA4hU/sKBMVZFhbVZ92yL5TkLWMFo\naE+jXeWTXE9/O8Qc63uCbqBFfiDVeXEgUlgPErzl3QyClH6/5MU5JCtidtDd9LAq\nN9e6uIMZvHLKyccxAms90L4br5kEFRt1E9DPkaACoQKBgQD5vtu7uDMvfFji28JR\nNkJaARU19yatjNuvtoOTGlglojV4jjyx+iq41Bs7OQsIbtGrCMIL9epgXxMc4b12\n2/9WXyceZN02JWw6nAJprep3rOHPXA1PKMjhBL4VOV/5hMKn8dkS9y6Fb664d725\nsqqHSv1kCvJpJL7Cew4dqUpOuwKBgQDVMC4KNQ/F37HKYi4NY+YNDP/P1yEG4ZCf\nfFyEXJr+PJ3LfTT58piggkJUijZNQM+OEFR7l37S+enHQ4M9FKZRXwmRvLRk/lrv\nmfJ539fyVToQEfi+/3MsjF+cb4NUMoAhpE5kiij4wrf+UO9h3azbUhzF2UieR//T\n+p682b92TwKBgDVYxnkHtK9NAXOb+5r7Wxr8pjo7y+BAeWDEPMC8XN3VE1ToFSDz\nThLjA9oXqjqn6VN+cGy7n8/sHxoJQj5UaetaMfH1G6eIQOEYGA/Y3X+oxydTA2jI\nTnh6WdwQwGZ9LFNRfsvlTuOj4o92zGkROAnkQ9IN4JADEFhcjrxZQA0nAoGBAKnv\n4vNOAsm3m9B43L7dwBbtIsl5ciE7Ev6eslzsOLyqcxovL1iCkjl4PAmJtulz3T8g\nM0flpjnk7v5hCa9Z044PlOAwLRhITRKrg8a0sT3BxCvlN4SAuj1rlBduKKCoNM0c\nXUT1gN1y0hoOSBOaEd0uIjNwFdveBsbiA0EEzgMvAoGAFzeOtTn9KxF+nDCiP1WQ\nzRAREahrUSlaPTDGQQh/Bc4mwzxAo9LV6wAvlILc8bQDAy2gMKayNGsngZNz/x4t\nmUIEhjDuqOxytT1lgrPJ5YcdXCANxTfeKbxqpAY1bE2096M+KRpuPA9vUHXjjZkZ\nhhBxutQbMAeIlXPAAjP3J8U=\n-----END PRIVATE KEY-----\n",
            "client_email": "alex-translator@fine-slice-382222.iam.gserviceaccount.com",
            "client_id": "110800149701420704171",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/alex-translator%40fine-slice-382222.iam.gserviceaccount.com"
        }
    )
    translate_client = translate.Client(credentials=creds)
    json_ls = json.loads(json_dic)
    for d in json_ls:
        data_old = d[target]
        result = translate_client.translate(data_old, target_language=to_language)
        new_data = result['translatedText']
        d[target] = new_data
    json_ls = json.dumps(json_ls, ensure_ascii=False)

    return json_ls

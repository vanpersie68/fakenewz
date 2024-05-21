import json
import random
import decimal

from django.http import JsonResponse, HttpResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from surveybuilder.serializers import SurveySerializer, QuestionSerializer, TextboxQuestionTextSerializer, \
    SocialPostQuestionSerializer, PostAddonfieldSerializer
from surveybuilder.views.survey_view import get_survey_data
from surveytaker.serializers import ResponseSerializer, ResponseQuestionSerializer, ResponseQuestionAnswerSerializer
from surveytaker.models import Response, ResponseBlock, ResponseQuestion, ResponseQuestionAnswer
from surveybuilder.models import Survey, Block, Question, TextboxQuestionText, SocialPostQuestion, PostAddonfield
from surveytaker.models import ResponseQuestion
from rest_framework.exceptions import NotFound, NotAcceptable


@swagger_auto_schema(operation_summary='get random responses', methods=['GET'])
@api_view(['GET'])
def get_text_result(request, flag, question_id):
    """
    get:
    Get 5 random responses or the latest 5 responses of a question, according to flag
    Flag (random:5 random responses  last:latest 5 responses)
    """
    print(flag)
    try:
        question = Question.objects.get(pk=question_id)
        question_serialized = QuestionSerializer(question)
        question_data = question_serialized.data
        question_id = question_data['id']
        response_questions = ResponseQuestion.objects.filter(question_id=question_id)
        response_questions_serialized = ResponseQuestionSerializer(response_questions, many=True)
        response_questions_data = response_questions_serialized.data
        answer_list = []
        news_post_answers = {}
        addons_list = []
        question_type = question_data['type']
        if question_type == 'News post':
            news_post = SocialPostQuestion.objects.get(question_id=question_id)
            news_post_serialized = SocialPostQuestionSerializer(news_post)
            news_post_data = news_post_serialized.data
            if news_post_data['numberAddon'] > 0:
                addons = PostAddonfield.objects.filter(postRow_id=news_post_data['id'])
                addons_serialized = PostAddonfieldSerializer(addons, many=True)
                addons_data = addons_serialized.data
                for addon in addons_data:
                    addon_data = {'id': addon['id'], 'postRow': addon['postRow'], 'title': addon['title'],
                                  'icon': addon['icon'], 'text': []}
                    addons_list.append(addon_data)
                news_post_answers['addon'] = addons_list
        for response_question in response_questions_data:
            q_id = response_question['id']
            answers = ResponseQuestionAnswer.objects.filter(question_id=q_id)
            answers_serialized = ResponseQuestionAnswerSerializer(answers, many=True)
            answers_data = answers_serialized.data
            for answers in answers_data:
                if question_type == 'Text entry':
                    text_entry = TextboxQuestionText.objects.get(question_id=question_id)
                    text_entry_serialized = TextboxQuestionTextSerializer(text_entry)
                    text_entry_data = text_entry_serialized.data
                    if 'ansType' in text_entry_data:
                        if text_entry_data['ansType'] == 'Text':
                            answer_list.append(answers['answerText'])
                        else:
                            answer_list.append(answers['answerDecimal'])
                elif question_type == 'News post':
                    if news_post_data['articleCommentsOn']:
                        if news_post_data['articleStyle'] == 'Twitter':
                            if answers['answerText'] is not '' and answers['title'] == 'Reply':
                                answer_list.append(answers['answerText'])
                        elif news_post_data['articleStyle'] == 'Facebook':
                            if answers['answerText'] is not '' and answers['title'] == 'Comment':
                                answer_list.append(answers['answerText'])
                    if news_post_data['numberAddon'] > 0:
                        for addon in news_post_answers['addon']:
                            if answers['title'] == addon['title'] and answers['answerText'] is not '':
                                addon['text'].append(answers['answerText'])
                        for addon in news_post_answers['addon']:
                            if len(addon['text']) > 5:
                                if flag == 'random':
                                    addon['text'] = random.sample(addon['text'], 5)
                                elif flag == 'last':
                                    addon['text'] = addon['text'][-5:]
                        if news_post_data['numberAddon'] == 2:
                            count = 1
                            for addon in news_post_answers['addon']:
                                news_post_answers['addOn' + str(count)] = addon['text']
                                count = count + 1
                        elif news_post_data['numberAddon'] == 1:
                            count = 1
                            for addon in news_post_answers['addon']:
                                news_post_answers['addOn' + str(count)] = addon['text']
                                count = count + 1
                            news_post_answers['addOn2'] = []
                    if news_post_data['numberAddon'] == 0:
                        news_post_answers['addOn1'] = []
                        news_post_answers['addOn2'] = []
                    if len(answer_list) > 5:
                        if flag == 'random':
                            answer_list = random.sample(answer_list, 5)
                        elif flag == 'last':
                            answer_list = answer_list[-5:]
                    news_post_answers['comments'] = answer_list
                else:
                    return JsonResponse({'Message': 'The question is not support.'}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    if question_type == 'Text entry':
        if len(answer_list) > 5:
            if flag == 'random':
                answer_list = random.sample(answer_list, 5)
            elif flag == 'last':
                answer_list = answer_list[-5:]
        return JsonResponse(answer_list, status=status.HTTP_200_OK, safe=False)
    elif question_type == 'News post':
        return JsonResponse(news_post_answers, status=status.HTTP_200_OK, safe=False)

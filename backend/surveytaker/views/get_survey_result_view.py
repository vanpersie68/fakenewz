import json
import random
import decimal
import datetime
import time

from django.http import JsonResponse, HttpResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from surveybuilder.serializers import SurveySerializer, QuestionSerializer
from surveybuilder.views.survey_view import get_survey_data
from surveytaker.serializers import ResponseSerializer, ResponseQuestionSerializer, ResponseQuestionAnswerSerializer, \
    ResponseBlockSerializer
from surveytaker.models import Response, ResponseBlock, ResponseQuestion, ResponseQuestionAnswer
from surveybuilder.models import Survey, Block, Question
from surveytaker.models import ResponseQuestion
from rest_framework.exceptions import NotFound, NotAcceptable


@swagger_auto_schema(operation_summary='get the statistic result of a survey', methods=['GET'])
@api_view(['GET'])
def get_result(request, preview, survey_id):
    """
    get:
    Get the statistic result of a survey
    Preview (1:preview result  0:user response result)
    """
    flag = False
    if preview == 1:
        flag = True
    try:
        responses = Response.objects.filter(survey=survey_id, preview=flag)
        # if len(responses) == 0:
        #     return JsonResponse({'Message': 'No response'}, status=status.HTTP_404_NOT_FOUND)
        responses_serialized = ResponseSerializer(responses, many=True)
        responses_data = responses_serialized.data
    except Response.DoesNotExist:
        return JsonResponse({'Message': 'No response'}, status=status.HTTP_404_NOT_FOUND)
    try:
        survey = Survey.objects.get(pk=survey_id)
        blocks = Block.objects.filter(survey=survey.id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    # get the information of the survey
    survey_data = get_survey_data(survey, blocks)
    count = len(Response.objects.filter(survey=survey_id, preview=flag))
    result = {'id': survey_data['id'], 'name': survey_data['name'], 'language': survey_data['language'],
              'time_limit_minutes': survey_data['time_limit_minutes'], 'status': survey_data['status'],
              'current_submission': survey_data['current_submission'],
              'required_submission': survey_data['required_submission'], 'create_time': survey_data['create_time'],
              'publish_time': survey_data['publish_time'], 'expire_time': survey_data['expire_time'],
              'is_repeat_answer': survey_data['is_repeat_answer'],
              'timeData': statistic_time(survey_id, responses_data),
              'browserData': statistic_browser(survey_id, responses_data)}
    blocks = []
    if 'blocks' in survey_data:
        blocks_data = survey_data['blocks']
        for block_data in blocks_data:
            block = {'id': block_data['id'], 'title': block_data['title'], 'order': block_data['order']}
            questions = []
            block['questions'] = questions
            if 'questions' in block_data:
                questions_data = block_data['questions']
                # find all questions
                for question_data in questions_data:
                    question_result = {'block': question_data['block'], 'order': question_data['order'],
                                       'required': question_data['required'],'type':question_data['type']}
                    # result[question_data['id']] = question_result
                    question_type = question_data['type']
                    # if question_type == 'Number scale':
                    #     x = [question_data['typedata']['minTitle'], question_data['typedata']['middleTitle'],
                    #          question_data['typedata']['maxTitle']]
                    #     question_result['x'] = x
                    get_answer(question_data, question_type, question_result, survey_id, flag, count)
                    questions.append(question_result)
            blocks.append(block)
    result['blocks'] = blocks
    for block in result['blocks']:
        for question in block['questions']:
            if question['type'] == 'Text entry':
                question['answered'] = len(question['answers'])
                if question['ansType'] == 'Integer' or question['ansType'] == 'Decimal':
                    if question['count'] > 0:
                        question['average'] = (
                            decimal.Decimal(sum(question['answers']) / len(question['answers']))).quantize(
                            decimal.Decimal("0.00"))
                    else:
                        question['average'] = 0
                if len(question['answers']) > 5:
                    question['answers'] = question['answers'][-5:]
            elif question['type'] == 'Number scale':
                y = []
                total = 0
                for number in question['numbers']:
                    if question['count'] > 0:
                        y.append(question['numbers'][number])
                        total = total + decimal.Decimal(number) * decimal.Decimal(question['numbers'][number])
                    else:
                        question['average'] = 0
                        y.append(0)
                    question['y'] = y
                if sum(y) > 0:
                    question['average'] = decimal.Decimal(total / sum(y)).quantize(
                        decimal.Decimal("0.00"))
                else:
                    question['average'] = 0
            elif question['type'] == 'Multiple choice':
                y = []
                for c in question['choices']:
                    if question['count'] > 0:
                        y.append(question['choices'][c])
                    else:
                        y.append(0)
                    question['y'] = y
            elif question['type'] == 'Button row':
                y = []
                for c in question['choices']:
                    if question['count'] > 0:
                        y.append(question['choices'][c])
                    else:
                        y.append(0)
                    question['y'] = y
            elif question['type'] == 'News post':
                question['typedata']['articleLikes'] = question.get('likes')
                question['typedata']['articleShares'] = question.get('shares')
                if 'comments' in question:
                    if len(question['comments']) > 5:
                        question['comments'] = question['comments'][-5:]
                if 'addon' in question:
                    for addon in question['addon']:
                        addon['count'] = len(addon['text'])
                        if len(addon['text']) > 5:
                            addon['text'] = addon['text'][-5:]
                if 'addon' not in question:
                    question['addon'] = []
    result['blocks'].sort(key=lambda x: x['order'])
    return JsonResponse(result, status=status.HTTP_200_OK, safe=False)


def is_preview(survey_id, flag):
    responses = Response.objects.filter(survey=survey_id, preview=flag)
    responses_serialized = ResponseSerializer(responses, many=True)
    responses_data = responses_serialized.data
    response_id = []
    for response in responses_data:
        response_id.append(response['id'])
    response_blocks = ResponseBlock.objects.filter(response_id__in=response_id)
    response_blocks_serialized = ResponseBlockSerializer(response_blocks, many=True)
    response_blocks_data = response_blocks_serialized.data
    response_block_id = []
    for response_block in response_blocks_data:
        response_block_id.append(response_block['id'])
    return response_block_id


def get_answer(question_data, question_type, question_result, survey_id, flag, count):
    # id of the question
    block_id = is_preview(survey_id, flag)
    question_id = question_data['id']
    response_questions = ResponseQuestion.objects.filter(question_id=question_id).filter(block_id__in=block_id)
    response_questions_serialized = ResponseQuestionSerializer(response_questions, many=True)
    response_questions_data = response_questions_serialized.data
    question_result['count'] = count
    question_result['question_id'] = question_id
    # id in database, use this id to find answers
    if question_type == 'News post':
        question_result['type'] = 'News post'
        question_result['typedata'] = question_data['typedata']
        if 'articleLikesOn' in question_data['typedata']:
            question_result['articleLikesOn'] = False
            if question_data['typedata']['articleLikesOn']:
                question_result['articleLikesOn'] = True
                question_result['likes'] = 0
        if 'articleSharesOn' in question_data['typedata']:
            question_result['articleSharesOn'] = False
            if question_data['typedata']['articleSharesOn']:
                question_result['articleSharesOn'] = True
                question_result['shares'] = 0
        if 'articleCommentsOn' in question_data['typedata']:
            question_result['articleCommentsOn'] = False
            if question_data['typedata']['articleCommentsOn']:
                question_result['articleCommentsOn'] = True
                comments = []
                question_result['comments'] = comments
        if 'numberAddon' in question_data['typedata']:
            if question_data['typedata']['numberAddon'] > 0:
                addons = []
                for addon in question_data['addon']:
                    addon_data = {'id': addon['id'], 'postRow': addon['postRow'], 'title': addon['title'],
                                  'icon': addon['icon'], 'text': []}
                    addons.append(addon_data)
                question_result['addon'] = addons
    elif question_type == 'Multiple choice':
        question_result['multipleAnswers'] = question_data['typedata']['multipleAnswers']
        question_result['otherInput'] = question_data['typedata']['otherInput']
        if question_result['otherInput']:
            Other = {'id': None, 'question': None, 'title': 'Other'}
            question_data['choices'].append(Other)
        if 'choices' in question_data:
            choices_data = question_data['choices']
            question_result['type'] = 'Multiple choice'
            question_result['title'] = question_data['name']
            choices = {}
            x = []
            for choice in choices_data:
                x.append(choice['title'])
                choices[choice['title']] = 0
            question_result['choices'] = choices
            question_result['x'] = x
    elif question_type == 'Matrix table':
        question_result['multipleAnswers'] = question_data['typedata']['multipleAnswers']
        question_result['otherInput'] = question_data['typedata']['otherInput']
        question_result['columnConfig'] = question_data['typedata']['columnConfig']
        question_result['tableConfig'] = question_data['typedata']['tableConfig']
    elif question_type == 'Groups':
        
        question_result['multipleAnswers'] = question_data['typedata']['multipleAnswers']
        question_result['otherInput'] = question_data['typedata']['otherInput']
        question_result['columnConfig'] = question_data['typedata']['columnConfig']
        question_result['tableConfig'] = question_data['typedata']['tableConfig']


    elif question_type == 'Button row':
        if 'buttons' in question_data:
            choices_data = question_data['buttons']
            question_result['type'] = 'Button row'
            question_result['title'] = question_data['name']
            choices = {}
            x = []
            for choice in choices_data:
                x.append(choice['buttonText'])
                choices[choice['buttonText']] = 0
            question_result['choices'] = choices
            question_result['x'] = x
    elif question_type == 'Number scale':
        if 'typedata' in question_data:
            interval = question_data['typedata']['interval']
            numberMax = question_data['typedata']['numberMax']
            numberMin = question_data['typedata']['numberMin']
            question_result['type'] = 'Number scale'
            question_result['title'] = question_data['name']
            numbers = {}
            x = []
            while numberMin <= numberMax:
                numbers[numberMin] = 0
                x.append(numberMin)
                numberMin = numberMin + interval
            question_result['numbers'] = numbers
            question_result['x'] = x
    elif question_type == 'Text entry':
        if 'typedata' in question_data:
            question_result['type'] = 'Text entry'
            question_result['title'] = question_data['name']
            question_result['ansType'] = question_data['typedata']['ansType']
            answers = []
            question_result['answers'] = answers

    for response_question in response_questions_data:
        q_id = response_question['id']
        answers = ResponseQuestionAnswer.objects.filter(question_id=q_id)
        answers_serialized = ResponseQuestionAnswerSerializer(answers, many=True)
        answers_data = answers_serialized.data
        # get all answers of a question
        for answer in answers_data:
            statistic(question_data, answer, question_type, question_result)


def statistic(question_data, answer, question_type, question_result):
    if question_type == 'News post':
        if question_data['typedata']['articleStyle'] == 'Twitter' \
                or question_data['typedata']['articleStyle'] == 'YouTube':
            if answer['title'] == 'Like' and answer['answerText'] == 'selected':
                question_result['likes'] = question_result['likes'] + 1
            elif answer['title'] == 'Retweet' and answer['answerText'] is not '':
                question_result['shares'] = question_result['shares'] + 1
            elif answer['title'] == 'Reply' and answer['answerText'] is not '':
                question_result['comments'].append(answer['answerText'])
            if 'addon' in question_result:
                for addon in question_result['addon']:
                    if answer['title'] == addon['title'] and answer['answerText'] is not '':
                        addon['text'].append(answer['answerText'])
        elif question_data['typedata']['articleStyle'] == 'Facebook':
            if answer['title'] == 'Like' and answer['answerText'] == 'selected':
                question_result['likes'] = question_result['likes'] + 1
            elif answer['title'] == 'Share' and answer['answerText'] is not '':
                question_result['shares'] = question_result['shares'] + 1
            elif answer['title'] == 'Comment' and answer['answerText'] is not '':
                question_result['comments'].append(answer['answerText'])
            if 'addons' in question_result:
                for addon in question_result['addons']:
                    if answer['title'] == addon['title'] and answer['answerText'] is not '':
                        addon['text'].append(answer['answerText'])
    elif question_type == 'Multiple choice':
        for choice in question_data['choices']:
            if answer['title'] == choice['title'] and answer['answerText'] == 'selected':
                question_result['choices'][choice['title']] = question_result['choices'][choice['title']] + 1
            elif answer['title'] == 'Other' and answer['answerText'] is not '' and choice['title'] == 'Other':
                question_result['choices']['Other'] = question_result['choices']['Other'] + 1
    elif question_type == 'Matrix table':
        if type(question_result.get('answers')) == list:
            dc = eval(answer['answerText'])
            question_result['answers'].append(json.dumps(dc))

        else: 
            question_result['answers'] = []
            dc = eval(answer['answerText'])
            question_result['answers'].append(json.dumps(dc))
    elif question_type == 'Groups':
        if type(question_result.get('answers')) == list:
            dc = eval(answer['answerText'])
            question_result['answers'].append(json.dumps(dc))

        else: 
            question_result['answers'] = []
            dc = eval(answer['answerText'])
            question_result['answers'].append(json.dumps(dc))
    elif question_type == 'Text entry':
        if question_result['ansType'] == 'Text' and answer['answerText'] is not '':
            question_result['answers'].append(answer['answerText'])
        elif question_result['ansType'] == 'Integer' and answer['answerDecimal'] is not '':
            question_result['answers'].append(decimal.Decimal((answer['answerDecimal'])))
        elif question_result['ansType'] == 'Decimal' and answer['answerDecimal'] is not '':
            question_result['answers'].append(decimal.Decimal((answer['answerDecimal'])))
    elif question_type == 'Number scale':
        for number in question_result['numbers']:
            if answer['title'] == question_result['title'] and answer['answerText'] == str(number):
                question_result['numbers'][number] = question_result['numbers'][number] + 1
    elif question_type == 'Button row':
        for choice in question_data['buttons']:
            if answer['title'] == choice['buttonText'] and answer['answerText'] == 'selected':
                question_result['choices'][choice['buttonText']] = question_result['choices'][choice['buttonText']] + 1


def statistic_time(survey_id, responses_data):
    if len(responses_data) == 0:
        timeData = {
            'minTime': 0,
            'midTime': 0,
            'maxTime': 0,
            'averageTime': 0
        }
        return timeData
    array_time = []
    for response in responses_data:
        end_datetime = str(response['end_datetime']).split('+')[0]
        create_datetime = str(response['create_datetime']).split('+')[0]
        end_date = end_datetime.split('T')[0]
        end_time = end_datetime.split('T')[1].split('Z')[0].split('.')[0]
        end = end_date + ' ' + end_time
        start_date = create_datetime.split('T')[0]
        start_time = create_datetime.split('T')[1].split('Z')[0].split('.')[0]
        start = start_date + ' ' + start_time
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        t = (end - start).total_seconds()
        array_time.append(int(t))
    array_time.sort()
    averageTime = sum(array_time) / len(array_time)
    minTime = min(array_time)
    maxTime = max(array_time)
    half = len(array_time) // 2
    midTime = array_time[half]
    timeData = {
        'minTime': round(minTime, 2),
        'midTime': round(midTime, 2),
        'maxTime': round(maxTime, 2),
        'averageTime': round(averageTime, 2)
    }
    return timeData


def statistic_browser(survey_id, responses_data):
    if len(responses_data) == 0:
        x = ['Chrome', 'Edge', 'Safari', 'Firefox', 'Other']
        y = [0, 0, 0, 0, 0]
        browserData = {
            'x': x,
            'y': y
        }
        return browserData
    dict_browser = {
        'Chrome': 0,
        'Edge': 0,
        'Safari': 0,
        'Firefox': 0,
        'Other': 0
    }
    for response in responses_data:
        user_agent = response['user_agent']
        if 'Chrome' in user_agent and 'Safari' in user_agent and 'Edg' not in user_agent:
            dict_browser['Chrome'] = dict_browser['Chrome'] + 1
        elif 'Edg' in user_agent:
            dict_browser['Edge'] = dict_browser['Edge'] + 1
        elif 'Safari' in user_agent and 'Chrome' not in user_agent:
            dict_browser['Safari'] = dict_browser['Safari'] + 1
        elif 'Firefox' in user_agent:
            dict_browser['Firefox'] = dict_browser['Firefox'] + 1
        else:
            dict_browser['Other'] = dict_browser['Other'] + 1
        x = []
        y = []
    for browser in dict_browser:
        x.append(browser)
        y.append(dict_browser[browser])
    browserData = {
        'x': x,
        'y': y
    }
    return browserData

import json
import csv
import operator
import ast

from django.http import JsonResponse, HttpResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from user_agents import parse

from surveybuilder.models import Survey, Question, TextboxQuestionText, Block
from surveybuilder.serializers import QuestionSerializer, SurveySerializer, \
    TextboxQuestionTextSerializer, BlockSerializer
from surveytaker.models import Response, ResponseBlock
from surveytaker.serializers import ResponseSerializer, ResponseBlockSerializer


@swagger_auto_schema(operation_summary='export response CSV file', methods=['GET'])
@api_view(['GET'])
def csv_export(request, survey_id):
    """
    get:
    Export all the responses and metadata of the survey in CSV format
    """
    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    survey_serialized = SurveySerializer(survey)
    survey_data = survey_serialized.data
    survey_name = survey_data['name']
    responses = Response.objects.filter(survey=survey.id).order_by('id')
    if len(responses) == 0:
        return JsonResponse({'code': 999, 'message': 'No response received yet!'})
    responses_serialized = ResponseSerializer(responses, many=True)
    responses_data = responses_serialized.data
    result = [[survey_data['name']]]
    last_title = []
    for response in responses_data:
        responses_blocks = ResponseBlock.objects.filter(response_id=response['id']).order_by('id')
        responses_blocks_serialized = ResponseBlockSerializer(responses_blocks, many=True)
        gaze_dict = {}
        click_dict = {}
        for responses_block in responses_blocks_serialized.data:
            block = Block.objects.get(pk=responses_block['block_id'])
            block_serialized = BlockSerializer(block)
            block_serialized_data = block_serialized.data
            block_name = block_serialized_data['title']
            gazeData = responses_block['gazeData']
            if gazeData != '[]':
                gaze_dict[block_name] = gazeData
            clickEvent = responses_block['clickEvent']
            if clickEvent is None:
                clickEvent = 'Not collected clickEvent.'
            click_dict[block_name] = clickEvent
        answer_json = json.loads(response['answer_json'])
        answer_row = [answer_json['respondent_identifier']]
        titles = ["respondent_identifier"]
        blocks = answer_json['response_blocks']
        for b in blocks:
            responses_questions = b['response_questions']
            for q in responses_questions:
                question_id = q['question_id']
                question = Question.objects.get(pk=question_id)
                question_serialized = QuestionSerializer(question)
                question_data = question_serialized.data
                title = 'q' + str(question_id) + '_' + question_data['name'].replace(' ', '_')
                if question_data['type'] != "Multiple choice" and \
                        question_data['type'] != "News post" and \
                        question_data['type'] != "Sliders" and \
                        question_data['type'] != "Groups" \
                        and title not in titles:
                    titles.append(title)
                if question_data['type'] == "Multiple choice":
                    rqa = q['response_question_answer']
                    answer_all = ""
                    for i in rqa:
                        if i['title'] == 'Other':
                            answer = i['answerText']
                        elif i['answerText'] == "selected":
                            answer = "True"
                        else:
                            answer = "False"
                        answer_all = answer_all + answer
                        title = title + ':' + i['title'] + ";"
                        # if title + ':' + i['title'] not in titles:
                        #     titles.append(title + ':' + i['title'])
                    titles.append(title)
                    answer_row.append(answer_all)
                # ke cheng
                if question_data['type'] == "Sliders":
                    all_data = q['response_question_answer']
                    slider_data = all_data[0]
                    answer_slider = ""
                    for i in slider_data['answerText']:
                        #     answer_slider = i['sliderVal']
                        #     titles.append(title + ':' + i['name'])
                        #     answer_row.append(answer_slider)
                        answer_slider = answer_slider + ";" + str(i['sliderVal'])
                        title = title + ':' + i['name']
                    answer_row.append(str(answer_slider))
                    titles.append(title)
                if question_data['type'] == "Groups":
                    gro_data = q['response_question_answer']
                    group_data = gro_data[0]
                    answer_group = ""
                    for i in group_data['answerText']:
                        children_ans = ''
                        children_data = i['children']
                        for j in children_data:
                            children_ans = children_ans + j['name']
                    #     titles.append(title + ':' + i['label'] + i['value'])
                    #     answer_row.append(children_ans)
                        title = title + ':' + i['label'] + i['value']
                        if children_ans == "":
                            answer_group = answer_group + "Empty ;"
                        else:
                            answer_group = answer_group + children_ans + ";"
                    answer_row.append(answer_group)
                    titles.append(title)



                if question_data['type'] == "Matrix table":
                    ma_data = q['response_question_answer']
                    ma_data = ma_data[0]
                    ma_k = ''
                    ma_d = ''
                    for key, value in ma_data['answerText'].items():
                        ma_k = ma_k + ";" +str(key)
                        # ma_d = ma_d + ' ' + str(value)
                    # titles.append(title + ':' + ma_k)
                    answer_row.append(ma_k)

                if question_data['type'] == "Rank order":
                    ma_data = q['response_question_answer']
                    ma_data = ma_data[0]
                    ma_data = ma_data['answerText']
                    rank_or = ''
                    rank_ti = ''
                    for i in ma_data:
                        rank_or = rank_or + " " + i['title']
                        rank_ti = rank_ti + str(i['order'])
                    answer_row.append(rank_ti + rank_or)

                if question_data['type'] == "Button row":
                    rqa = q['response_question_answer']
                    answer = 'Not collected.'
                    for i in rqa:
                        if i['answerText'] == "selected":
                            answer = answer + i['title'] + ' '
                    answer_row.append(answer[:len(answer) - 1])
                if question_data['type'] == "Text entry":
                    questionText = TextboxQuestionText.objects.get(question=q['question_id'])
                    questionText_serializer = TextboxQuestionTextSerializer(questionText)
                    questionText_data = questionText_serializer.data
                    if questionText_data['ansType'] == 'Text':
                        answer = q['response_question_answer'][0]['answerText']
                    else:
                        answer = q['response_question_answer'][0]['answerDecimal']
                    answer_row.append(answer)
                if question_data['type'] == "Number scale":
                    answer = q['response_question_answer'][0]['answerText']
                    answer_row.append(str(answer))
                if question_data['type'] == "News post":
                    abcd = []
                    temp_ans = ''
                    rqa = q['response_question_answer']
                    for i in rqa:
                        if i['answerText'] is not None:
                            temp_ans = temp_ans + i['title'] + ":" + str(i['answerText']) + "; "
                        else:
                            temp_ans = temp_ans + i['title'] + ":" + 'Not collected.' + "; "

                        if title not in titles:
                            titles.append(title)
                        abcd.append(temp_ans)
                    answer_row.append(abcd)
        # change order of different questions   response['questionsOrder']
        answer_row = reverse_random(answer_row, response['questionsOrder'])

        if response['questionsOrder'] is not None:
            answer_row.append(response['questionsOrder'])
        else:
            answer_row.append('Not added questionsOrder!')

        answer_row.append(response['create_datetime'][0:10] + " " + response['create_datetime'][11:19])
        answer_row.append(response['end_datetime'][0:10] + " " + response['end_datetime'][11:19])
        answer_row.append(response['preview'])
        answer_row.append(response['completion_rate'])
        if response['camera_state']:
            answer_row.append('Valid')
        else:
            answer_row.append('Invalid')
        if 'user_agent' in answer_json:
            user_agent = parse(answer_json['user_agent'])
            answer_row.append(user_agent.device)
            answer_row.append(user_agent.os.family)
            answer_row.append(user_agent.os.version_string)
            answer_row.append(user_agent.browser.family)
            answer_row.append(user_agent.browser.version_string)
        answer_row.append(json.dumps(click_dict))
        if not gaze_dict:
            answer_row.append("Not collected")
        else:
            answer_row.append(json.dumps(gaze_dict))
        if 'user_action' in answer_json:
            if answer_json['user_action'] == '[]':
                answer_json['user_action'] = 'Not Collected.'
            answer_row.append(answer_json['user_action'])
        # kecheng
        if response['screen_size']:
            answer_row.append(response['screen_size'])
        else:
            answer_row.append('Not collected')

        if response['calibration_acc'] is not None:
            answer_row.append(response['calibration_acc'])

        # change the order of the title of different questions
        titles = reverse_random(titles, response['questionsOrder'])
        titles.append("questionsOrder")
        titles.append("create_time")
        titles.append("end_time")
        titles.append("is_preview")
        titles.append("completion_rate")
        titles.append("camera_state")
        titles.append("device")
        titles.append("os")
        titles.append("os_version")
        titles.append("browser")
        titles.append("browser_version")
        titles.append("click_event")
        titles.append("gaze_data")
        titles.append("user_action")
        titles.append("screen_size")
        titles.append("calibration_acc")

        if not operator.eq(titles, last_title):
            result.append(titles)
            last_title = titles
        result.append(answer_row)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + survey_name + '_export_result.csv'
    writer = csv.writer(response)
    for i in result:
        writer.writerow(i)
    return response


def reverse_random(lst, order):
    if order is None:
        return lst
    order_dict = ast.literal_eval(order)
    orders = [order_dict[k] for k in order_dict]

    start = 1
    result = []
    for l in orders:
        result.append(lst[start:start + len(l)])
        start += len(l)

    new_result = []
    for i in range(len(orders)):
        sublist = ['']*len(orders[i])
        for index, j in enumerate(orders[i]):
            sublist[j-1] = result[i][index]
        new_result.append(sublist)

    new_result.insert(0, lst[0])
    flat_list = [item for sublist in new_result for item in (sublist if isinstance(sublist, list) else [sublist])]
    return flat_list


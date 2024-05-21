from django.http import JsonResponse
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from surveytaker.models import Response, ResponseBlock, ResponseQuestion, ResponseQuestionAnswer
from surveybuilder.models import Survey, Block, Question

@swagger_auto_schema(
    request_body=openapi.Schema(
    title="Response",
    type=openapi.TYPE_OBJECT,
    properties={
                'uuid': openapi.Schema(type=openapi.TYPE_STRING),
                'respondent_identifier': openapi.Schema(type=openapi.TYPE_STRING),
                'survey_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'researcher': openapi.Schema(type=openapi.TYPE_INTEGER),
                'create_time': openapi.Schema(type=openapi.TYPE_STRING),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING),
                'completion_rate': openapi.Schema(type=openapi.TYPE_STRING),
                'user_agent': openapi.Schema(type=openapi.TYPE_STRING),
                'user_action': openapi.Schema(type=openapi.TYPE_STRING),
                'preview': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'screen_size': openapi.Schema(type=openapi.TYPE_STRING),
                'calibration_acc': openapi.Schema(type=openapi.TYPE_STRING),
                'questionsOrder': openapi.Schema(type=openapi.TYPE_STRING),
                'response_blocks': openapi.Schema(type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_OBJECT)),
    }),
    operation_summary='save survey taker\'s response to database', methods=['POST'])
@api_view(['POST'])
def save_response(request):
    """
    POST:
    Save survey taker's response to database
    """
    json = request.body.decode()
    data = request.data
    if request.method == 'POST':
        try:
            survey_id = data['survey_id']
            survey = Survey.objects.get(id=survey_id)
            count = Response.objects.filter(uuid=data['uuid']).count()
            if count > 0:
                update_flag = True
            else:
                update_flag = False
            required_submission = survey.required_submission
            current_submission = survey.current_submission
            statue = survey.status
            try:
                if statue == 1:
                    if not update_flag:
                        save_data(data, json)
                        survey.current_submission = current_submission + 1
                    else:
                        update_data(data, json)
                    survey.save()
                    if required_submission != 0 and survey.current_submission == required_submission:
                        survey.status = 2
                        survey.save()
                        return JsonResponse({"Message": "The survey is full, survey is now closed"},
                                            status=status.HTTP_200_OK)
                    return JsonResponse({"Message": "success"}, status=status.HTTP_200_OK)
                elif statue == 0:
                    if not update_flag:
                        save_data(data, json)
                    else:
                        update_data(data, json)
                    return JsonResponse({"Message": "preview model, success"}, status=status.HTTP_200_OK)
                else:
                    return JsonResponse({'Message': 'The survey has already full.'}, status=status.HTTP_200_OK)
            except Exception:
                raise Exception
                # return JsonResponse({'Message': 'The json format is wrong.'}, status=status.HTTP_403_FORBIDDEN)
        except Survey.DoesNotExist:
            return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)


def save_data(data, json):
    response = Response()
    if 'survey_id' in data:
        response.survey = data['survey_id']
    if 'create_datatime' in data:
        response.create_datetime = data['create_datatime']
    if 'end_datatime' in data:
        response.end_datetime = data['end_datatime']
    if 'contact_info' in data:
        response.contact_info = data['contact_info']
    if 'user_agent' in data:
        response.user_agent = data.get('user_agent')
    if 'user_action' in data:
        response.user_action = data.get('user_action')
    if 'respondent_identifier' in data:
        response.respondent_identifier = data['respondent_identifier']
    if 'preview' in data:
        response.preview = data['preview']
    if 'completion_rate' in data:
        response.completion_rate = data['completion_rate']
    if 'camera_state' in data:
        response.camera_state = data['camera_state']
    if 'uuid' in data:
        response.uuid = data['uuid']
    if 'screen_size' in data:
        response.screen_size = data.get('screen_size')
        # response.screen_size = data['screen_size']
    if 'calibration_acc' in data:
        response.calibration_acc = data.get('calibration_acc')
    if 'questionsOrder' in data:
        data = data.get('questionsOrder')
        result = {}
        for i, arr in enumerate(data):
            block_name = "Block" + str(i + 1)
            result[block_name] = arr
        response.questionsOrder = result

    response.answer_json = json
    response.save()
    if 'response_blocks' in data:
        for response_block in data['response_blocks']:
            responseBlock = ResponseBlock()
            responseBlock.response = response
            if 'block_id' in response_block:
                block = Block.objects.get(id=response_block['block_id'])
                responseBlock.block = block
            responseBlock.create_datetime = response_block.get('createTime')
            responseBlock.end_datetime = response_block.get('endTime')
            responseBlock.gazeData = response_block.get('gazeData')
            responseBlock.clickEvent = response_block.get('clickEvent')
            responseBlock.uuid = response_block.get('uuid')
            responseBlock.save()
            if 'response_questions' in response_block:
                response_questions = response_block['response_questions']
                for response_question in response_questions:
                    responseQuestion = ResponseQuestion()
                    responseQuestion.block = responseBlock
                    if 'question_id' in response_question:
                        question = Question.objects.get(id=response_question['question_id'])
                        responseQuestion.question = question
                    responseQuestion.save()
                    if 'response_question_answer' in response_question:
                        response_question_answers = response_question['response_question_answer']
                        for response_question_answer in response_question_answers:
                            responseQuestionAnswer = ResponseQuestionAnswer()
                            responseQuestionAnswer.question = responseQuestion
                            if 'title' in response_question_answer:
                                responseQuestionAnswer.title = response_question_answer['title']
                            if 'answerText' in response_question_answer:
                                answerText = response_question_answer['answerText']
                                if answerText is not None:
                                    responseQuestionAnswer.answerText = answerText
                            if 'answerDecimal' in response_question_answer:
                                answerDecimal = response_question_answer['answerDecimal']
                                if answerDecimal is not None:
                                    responseQuestionAnswer.answerDecimal = answerDecimal
                            responseQuestionAnswer.uuid = response_question_answer['uuid']
                            responseQuestionAnswer.save()


def update_data(data, json):
    response = Response.objects.get(uuid=data['uuid'])
    if 'survey_id' in data:
        response.survey = data['survey_id']
    if 'create_datatime' in data:
        response.create_datetime = data['create_datatime']
    if 'end_datatime' in data:
        response.end_datetime = data['end_datatime']
    if 'contact_info' in data:
        response.contact_info = data['contact_info']
    if 'user_agent' in data:
        response.user_agent = data.get('user_agent')
    if 'user_action' in data:
        response.user_action = data.get('user_action')
    if 'respondent_identifier' in data:
        response.respondent_identifier = data['respondent_identifier']
    if 'preview' in data:
        response.preview = data['preview']
    if 'completion_rate' in data:
        response.completion_rate = data['completion_rate']
    if 'camera_state' in data:
        response.camera_state = data['camera_state']
    if 'uuid' in data:
        response.uuid = data['uuid']
    # ke cheng
    if 'screen_size' in data:
        response.screen_size = data.get('screen_size')
        # response.screen_size = data['screen_size']
    if 'calibration_acc' in data:
        response.calibration_acc = data.get('calibration_acc')
    if 'questionsOrder' in data:
        data = data.get('questionsOrder')
        result = {}
        for i, arr in enumerate(data):
            block_name = "Block" + str(i + 1)
            result[block_name] = arr
        response.questionsOrder = result

    response.answer_json = json
    response.save()
    if 'response_blocks' in data:
        for response_block in data['response_blocks']:
            response_block_count = ResponseBlock.objects.filter(uuid=response_block['uuid']).count()
            if response_block_count > 0:
                responseBlock = ResponseBlock.objects.get(uuid=response_block['uuid'])
            else:
                responseBlock=ResponseBlock()
            responseBlock.response = response
            if 'block_id' in response_block:
                block = Block.objects.get(id=response_block['block_id'])
                responseBlock.block = block
            responseBlock.create_datetime = response_block.get('createTime')
            responseBlock.end_datetime = response_block.get('endTime')
            responseBlock.gazeData = response_block.get('gazeData')
            responseBlock.clickEvent = response_block.get('clickEvent')
            responseBlock.uuid = response_block.get('uuid')
            responseBlock.save()
            if 'response_questions' in response_block:
                response_questions = response_block['response_questions']
                for response_question in response_questions:
                    responseQuestion = ResponseQuestion()
                    responseQuestion.block = responseBlock
                    if 'question_id' in response_question:
                        question = Question.objects.get(id=response_question['question_id'])
                        responseQuestion.question = question
                    responseQuestion.save()
                    if 'response_question_answer' in response_question:
                        response_question_answers = response_question['response_question_answer']
                        for response_question_answer in response_question_answers:
                            print(response_question_answer)
                            response_question_answer_count = ResponseQuestionAnswer.objects.filter(
                                uuid=response_question_answer['uuid']).count()
                            if response_question_answer_count > 0:
                                responseQuestionAnswer = ResponseQuestionAnswer.objects.get(
                                    uuid=response_question_answer['uuid'])
                            else:
                                responseQuestionAnswer = ResponseQuestionAnswer()
                            responseQuestionAnswer.question = responseQuestion
                            if 'title' in response_question_answer:
                                responseQuestionAnswer.title = response_question_answer['title']
                            if 'answerText' in response_question_answer:
                                answerText = response_question_answer['answerText']
                                if answerText is not None:
                                    responseQuestionAnswer.answerText = answerText
                            if 'answerDecimal' in response_question_answer:
                                answerDecimal = response_question_answer['answerDecimal']
                                if answerDecimal is not None:
                                    responseQuestionAnswer.answerDecimal = answerDecimal
                            responseQuestionAnswer.uuid = response_question_answer['uuid']
                            responseQuestionAnswer.save()

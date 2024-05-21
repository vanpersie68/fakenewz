import string
import random
from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.const import questionTypeModel, questionTypeSerializer
from surveybuilder.models import Survey, Block, Question, MultiChoiceQuestion, MultiChoice, \
    RankOrderQuestion, RankOrder,\
    MatrixTableQuestion, MatrixTable,SlidersQuestion, Sliders,GroupsQuestion, Groups,\
    ButtonRowQuestion, ButtonQuestion, PostAddonfield, SocialPostQuestion, RandomSections,Comment
from surveytaker.models import Response, ResponseBlock, ResponseQuestion, ResponseQuestionAnswer
from surveytaker.serializers import ResponseSerializer, ResponseQuestionSerializer, ResponseQuestionAnswerSerializer, \
    ResponseBlockSerializer
from surveybuilder.serializers import SurveySerializer, BlockSerializer, QuestionSerializer, \
    MultiChoiceSerializer, ButtonQuestionSerializer, PostAddonfieldSerializer, RadomSectionsSerializer,RankOrderSerializer,MatrixTableSerializer,SlidersSerializer,GroupsSerializer,CommentSerializer
from django.db.models import Q


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Survey',
        type=openapi.TYPE_OBJECT,
        properties={'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'researcher': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'language': openapi.Schema(type=openapi.TYPE_STRING),
                    'consentText': openapi.Schema(type=openapi.TYPE_STRING),
                    'current_submission': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'required_submission': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'time_limit_minutes': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'create_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'publish_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'expire_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_repeat_answer': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'if_capture_gaze': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'duration': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'code': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Include a new button entity to a postAddonField entity',
    methods=['POST']
)
@api_view(['POST'])
def create_survey(request):
    """
    post:
    Include a new survey to the database
    """
    # POST a new survey!
    parsed_request = JSONParser().parse(request)
    survey_serialized = SurveySerializer(data=parsed_request)

    if survey_serialized.is_valid():
        survey_serialized.save()
        return JsonResponse(survey_serialized.data, status=status.HTTP_201_CREATED)
    return JsonResponse(survey_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='Return surveys created by the researcher', methods=['GET'])
@api_view(['GET'])
def survey_list(requset, researcher_id):
    """
    get:
    Return surveys created by the researcher
    """
    condition1 = Q(researcher_id=researcher_id)
    condition2 = Q(collaborator__contains=[researcher_id])

    surveys = Survey.objects.filter(condition1 | condition2).filter(deleted=False)
    # surveys = Survey.objects.filter(researcher_id=researcher_id).filter(deleted=False)

    survey_serialized = SurveySerializer(surveys, many=True)
    return JsonResponse(survey_serialized.data, safe=False)


@swagger_auto_schema(operation_summary='Return surveys in trash bin which created by the researcher', methods=['GET'])
@api_view(['GET'])
def survey_deleted_list(requset, researcher_id):
    """
    get:
    Return surveys in trash bin which created by the researcher
    """
    surveys = Survey.objects.filter(researcher_id=researcher_id).filter(deleted=True)
    survey_serialized = SurveySerializer(surveys, many=True)
    return JsonResponse(survey_serialized.data, safe=False)


@swagger_auto_schema(
    operation_summary='Get a specific survey and all nested data. This includes blocks, questions, questions types, and all relevant data.',
    methods=['GET'])
@api_view(['GET'])
def survey_data(request, id):
    """
    get:
    Get a specific survey and all nested data. This includes blocks, questions, questions types, and all relevant data.
    """
    try:
        survey = Survey.objects.get(pk=id)
        blocks = Block.objects.filter(survey=survey.id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    survey_data = get_survey_data(survey, blocks)
    return JsonResponse(survey_data, safe=False)


@swagger_auto_schema(operation_summary='Get a specific survey by its ID', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Survey',
        type=openapi.TYPE_OBJECT,
        properties={'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'researcher': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'language': openapi.Schema(type=openapi.TYPE_STRING),
                    'consentText': openapi.Schema(type=openapi.TYPE_STRING),
                    'current_submission': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'required_submission': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'time_limit_minutes': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'status': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'create_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'publish_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'expire_time': openapi.Schema(type=openapi.TYPE_STRING),
                    'is_repeat_answer': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'if_capture_gaze': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'duration': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'code': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update a specific survey by its ID',
    methods=['PATCH']
)
@swagger_auto_schema(operation_summary='Delete a specific survey by its ID', methods=['DELETE'])
@api_view(['GET', 'PATCH', 'DELETE'])
def survey_info(request, id):
    """
    get:
    Get a specific survey by its ID

    patch:
    Update a specific survey by its ID

    delete:
    Delete a specific survey by its ID
    """
    try:
        survey = Survey.objects.get(pk=id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a specific survey

        survey_serialized = SurveySerializer(survey)
        return JsonResponse(survey_serialized.data)
    elif request.method == 'DELETE':
        # DELETE a specific survey

        survey.delete()
        status_code = survey.status
        if status_code == 1 or status_code == 2:
            try:
                responses = Response.objects.filter(survey=id)
                responses.delete()
            except Response.DoesNotExist:
                pass
        return JsonResponse({'Message': 'The survey has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        # UPDATE a specific survey

        parsed_request = JSONParser().parse(request)
        survey_serialized = SurveySerializer(survey, data=parsed_request, partial=True)
        if 'deleted' in parsed_request:
            deleted = parsed_request['deleted']
            if survey_serialized.is_valid():
                if deleted == 1 and survey.status == 1:
                    status_json = {"deleted": True, "status": 2}
                    survey_serialized = SurveySerializer(survey, data=status_json, partial=True)

        if survey_serialized.is_valid():
            survey_serialized.save()
            return JsonResponse(survey_serialized.data)
        return JsonResponse(survey_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='Get a specific survey code by its ID', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Code',
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='add a random code to the survey',
    methods=['POST']
)
@api_view(['GET', 'POST'])
def survey_code(request, id):
    """
    get:
    Get a specific survey code by its ID

    post:
    add a random code to the survey

    """
    try:
        survey = Survey.objects.get(pk=id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Get a specific survey code by its ID
        survey_serialized = SurveySerializer(survey)
        survey_data = survey_serialized.data
        result = {}
        result['code'] = survey_data['code']
        return JsonResponse(result)
    elif request.method == 'POST':
        # Post a random code to the survey
        survey_serialized = SurveySerializer(survey, data={}, partial=True)
        ran_code = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        if survey_serialized.is_valid():
            survey_data = survey_serialized.validated_data
            survey_data['code'] = ran_code
            survey_serialized.save()
            return JsonResponse(survey_serialized.data)
        return JsonResponse(survey_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


def get_survey_data(survey, blocks):
    # Transform data into python native
    survey_serialized = SurveySerializer(survey)
    blocks_serialized = BlockSerializer(blocks, many=True)
    # Extract data
    survey_data = survey_serialized.data
    survey_data['blocks'] = blocks_serialized.data[:]
    randomSections = RandomSections.objects.filter(survey=survey.id)
    randomSections_serialized = RadomSectionsSerializer(randomSections, many=True)
    randomSections_data = randomSections_serialized.data
    result = []
    for (i, rs) in enumerate(randomSections_data):
        subset = {'display': rs['display'], 'startWith': rs['startWith'], 'endWith': rs['endWith'],
                  'index': rs['index']}
        result.append(subset)
    survey_data['randomSections'] = randomSections_data[:]
    # Includes all question data
    for (i, bloc) in enumerate(blocks):
        questions = Question.objects.filter(block=bloc.id)
        questions_serialized = QuestionSerializer(questions, many=True)
        survey_data['blocks'][i]['questions'] = questions_serialized.data[:]
        # Includes all question subtype data
        for (i, ques) in enumerate(survey_data['blocks'][i]['questions']):
            questiontype = questionTypeModel[ques['type']].objects.get(question=ques['id'])
            questiontype_serialized = questionTypeSerializer[ques['type']](questiontype)
            ques['typedata'] = questiontype_serialized.data
            comments = Comment.objects.filter(question=ques['id'])
            ques['comments'] = CommentSerializer(comments,many=True).data

            if ques['type'] == 'Multiple choice':
                multichoice = MultiChoiceQuestion.objects.get(question=ques['id'])
                choices = MultiChoice.objects.filter(question=multichoice.id).order_by('order')
                choicesSerialized = MultiChoiceSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Rank order':
                ro = RankOrderQuestion.objects.get(question=ques['id'])
                choices = RankOrder.objects.filter(question=ro.id).order_by('order')
                choicesSerialized = RankOrderSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Matrix table':
                mt = MatrixTableQuestion.objects.get(question=ques['id'])
                choices = MatrixTable.objects.filter(question=mt.id).order_by('order')
                choicesSerialized = MatrixTableSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Sliders':
                mt = SlidersQuestion.objects.get(question=ques['id'])
                choices = Sliders.objects.filter(question=mt.id).order_by('order')
                choicesSerialized = SlidersSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Groups':
                mt = GroupsQuestion.objects.get(question=ques['id'])
                choices = Groups.objects.filter(question=mt.id).order_by('order')
                choicesSerialized = GroupsSerializer(choices, many=True)
                ques['choices'] = choicesSerialized.data[:]
            elif ques['type'] == 'Button row':
                buttonrow = ButtonRowQuestion.objects.get(question=ques['id'])
                buttons = ButtonQuestion.objects.filter(buttonRow=buttonrow.id)
                buttonsSerialized = ButtonQuestionSerializer(buttons, many=True)
                ques['buttons'] = buttonsSerialized.data[:]
            elif ques['type'] == 'News post':
                socialPost = SocialPostQuestion.objects.get(question=ques['id'])
                addon = PostAddonfield.objects.filter(postRow=socialPost.id)
                addonSerialized = PostAddonfieldSerializer(addon, many=True)
                ques['addon'] = addonSerialized.data[:]

    return survey_data


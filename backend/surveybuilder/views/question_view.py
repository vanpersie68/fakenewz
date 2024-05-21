from operator import delitem
from django.http import JsonResponse
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from surveybuilder.const import questionTypeSerializer, questionTypeModel
from surveybuilder.models import Block, Question, MultiChoice, ButtonQuestion, DragAndDropCard, DragAndDropChoice, \
    PostAddonfield,Comment
from surveybuilder.serializers import QuestionSerializer,CommentSerializer


@swagger_auto_schema(operation_summary='Get all questions within a specific block', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Question',
        type=openapi.TYPE_OBJECT,
        properties={'block': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'required': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'image': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Include a question into a specific block, this also automatically creates the question subtype',
    methods=['POST']
)
@api_view(['GET', 'POST'])
def question_list(request, id):
    """
    get:
    Get all questions within a specific block

    post:
    Include a question into a specific block, this automatically creates the question subtype as well
    """
    try:
        # Needs to include some sort of authentication check here
        block = Block.objects.get(pk=id)
    except Block.DoesNotExist:
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET list of blocks in a block

        questions = Question.objects.filter(block=block.id)
        questions_serialized = QuestionSerializer(questions, many=True)
        return JsonResponse(questions_serialized.data, safe=False)
    elif request.method == 'POST':
        # POST new question to the block

        parsed_request = JSONParser().parse(request)
        parsed_request["block"] = block.id

        if parsed_request["type"] not in questionTypeSerializer:
            return JsonResponse({'Message': 'Incorrect question type.'}, status=status.HTTP_400_BAD_REQUEST)

        question_serialized = QuestionSerializer(data=parsed_request)

        if question_serialized.is_valid():
            question_serialized.save()
        else:
            JsonResponse(question_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create an empty question
        questionType_data = {"question": question_serialized.data['id']}
        # Try serialize it..
        questionType_serialized_data = questionTypeSerializer[question_serialized.data['type']](data=questionType_data)

        if questionType_serialized_data.is_valid():
            questionType_serialized_data.save()
        else:
            return JsonResponse(questionType_serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse(question_serialized.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Question',
        type=openapi.TYPE_OBJECT,
        properties={'block': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'required': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'image': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary=' Takes an existing question ID and duplicates it, include order for the new question object',
    methods=['POST']
)
@api_view(['POST'])
def duplication_question(request, id):
    """
    post:
    Takes an existing question ID and duplicates it
    {
      order: "include order for the new question object"
    }
    """
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # parse request information to find new question order
        parsed_request = JSONParser().parse(request)

        # create a copy of the subtype information
        questionTypeInformation = questionTypeModel[question.type].objects.get(question=question.id)

        # if multi-choice, button-row or drag and drop get sub-sub-type information
        if (question.type == "Multiple choice"):
            # get a copy of all choices
            choices = MultiChoice.objects.filter(question=questionTypeInformation.id)
        elif (question.type == "Button row"):
            # get a copy of all buttons
            buttons = ButtonQuestion.objects.filter(buttonRow=questionTypeInformation.id)
        elif (question.type == "News post"):
            # get a copy of all buttons
            postAddons = PostAddonfield.objects.filter(postRow=questionTypeInformation.id)
        elif (question.type == "Drag and drop"):
            # get copy of all cards
            drag_cards = DragAndDropCard.objects.filter(question=questionTypeInformation.id)
            # then get copy of all choices
            drag_choices = DragAndDropChoice.objects.filter(question=questionTypeInformation.id)

        # create a copy of the question information
        question.id = None
        questionTypeInformation.id = None

        try:
            question.order = parsed_request['order']
            question.save()
            questionTypeInformation.question = question
            questionTypeInformation.save()
            if (question.type == "Multiple choice"):
                for entry in choices:
                    entry.id = None
                    entry.question = questionTypeInformation
                    entry.save()
            elif (question.type == "Button row"):
                for entry in buttons:
                    entry.id = None
                    entry.buttonRow = questionTypeInformation
                    entry.save()
            elif (question.type == "News post"):
                for entry in postAddons:
                    entry.id = None
                    entry.postRow = questionTypeInformation
                    entry.save()
            elif (question.type == "Drag and drop"):
                for entry1 in drag_cards:
                    entry1.id = None
                    entry1.question = questionTypeInformation
                    entry1.save()
                for entry2 in drag_choices:
                    entry2.id = None
                    entry2.question = questionTypeInformation
                    entry2.save()
        except Exception as e:
            return JsonResponse({'Message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        question_serialized = QuestionSerializer(question)
        return JsonResponse(question_serialized.data, status=status.HTTP_201_CREATED, safe=False)


@swagger_auto_schema(operation_summary='Get all question information by a specific ID', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Question',
        type=openapi.TYPE_OBJECT,
        properties={'block': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'required': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'image': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update a questions information given its ID',
    methods=['PATCH']
)
@swagger_auto_schema(operation_summary='Remove a question by ID', methods=['DELETE'])
@api_view(['GET', 'PATCH', 'DELETE'])
def question_info(request, id):
    """
    get:
    Get all question information by a specific ID

    patch:
    Update a questions' information given its ID

    delete:
    Remove a question by ID
    """
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a specific question

        question_serialized = QuestionSerializer(question)
        questiontype = questionTypeModel[question_serialized.data['type']].objects.get(question=question.id)
        questiontype_serialized = questionTypeSerializer[question_serialized.data['type']](questiontype)

        question_data = question_serialized.data
        question_data['type'] = questiontype_serialized.data
        comments = Comment.objects.filter(question=question_data['id'])
        question_data['type']['comments'] = CommentSerializer(comments,many=True).data
        return JsonResponse(question_data, safe=False)
    elif request.method == 'DELETE':
        # DELETE a specific question

        question.delete()
        return JsonResponse({'Message': 'The question has been deleted.'}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        # UPDATE a specific question

        parsed_request = JSONParser().parse(request)
        question_serialized = QuestionSerializer(question, data=parsed_request, partial=True)

        if question_serialized.is_valid():
            question_serialized.save()
            return JsonResponse(question_serialized.data)
        return JsonResponse(question_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Question',
        type=openapi.TYPE_OBJECT,
        properties={'block': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'type': openapi.Schema(type=openapi.TYPE_STRING),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'required': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'image': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update question subtype information by ID',
    methods=['PATCH']
)
@api_view(['PATCH'])
def question_inner(request, id):
    """
    patch:
    Update question subtype information by ID
    """
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    # Parse the request passed through
    parsed_request = JSONParser().parse(request)

    # Associate the ID key to a questions data and find its type
    question_serialized = QuestionSerializer(question)
    questiontype = questionTypeModel[question_serialized.data['type']].objects.get(question=question.id)

    # Serialize the request
    parsed_request_serialized = questionTypeSerializer[question_serialized.data['type']](questiontype,
                                                                                         data=parsed_request,
                                                                                         partial=True)

    if parsed_request_serialized.is_valid():
        parsed_request_serialized.save()
        return JsonResponse(parsed_request_serialized.data)
    return JsonResponse(parsed_request_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Question',
        type=openapi.TYPE_OBJECT,
        properties={
            'image': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update question image by ID',
    methods=['PATCH']
)
@api_view(['PATCH'])
def question_image(request, id):
    """
    patch:
    Update question image by ID
    """
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    # Parse the request passed through
    parsed_request = JSONParser().parse(request)
    question.image = parsed_request.get("image")
    # Associate the ID key to a questions data and find its type
    question.save()
    question_serialized = QuestionSerializer(question)
    return JsonResponse(question_serialized.data)

@api_view(['POST','DELETE','PATCH'])
def comment(request, id):

    if request.method == 'DELETE':
        obj = Comment.objects.get(pk=id)
        obj.delete()
        return JsonResponse({'code': 0})
    if request.method == 'PATCH':
        obj = Comment.objects.get(pk=id)
        parsed_request = JSONParser().parse(request)

        obj.content = parsed_request.get('content') or obj.content
        obj.username = parsed_request.get('username') or obj.username
        obj.avatarUrl = parsed_request.get('avatarUrl') or obj.avatarUrl
        obj.save()
        comment_serialized = CommentSerializer(obj)
        return JsonResponse({'code': 0, 'value': comment_serialized.data})

    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    parsed_request = JSONParser().parse(request)

    if request.method == 'POST':
        print({'question': question.id, 'content': parsed_request.get('content')})
        comment_serialized = CommentSerializer(data={'question': question.id, 'content': parsed_request.get('content')})
        if comment_serialized.is_valid():
            comment_serialized.save()
            return JsonResponse(comment_serialized.data)
        return JsonResponse(comment_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

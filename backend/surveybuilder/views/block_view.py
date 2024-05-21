from django.http import JsonResponse
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from surveybuilder.const import questionTypeModel
from surveybuilder.models import Survey, Block, Question, MultiChoice, ButtonQuestion, DragAndDropCard, \
    DragAndDropChoice
from surveybuilder.serializers import BlockSerializer


@swagger_auto_schema(operation_summary='Get all blocks within a survey', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Block',
        type=openapi.TYPE_OBJECT,
        properties={'survey': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Include a block to a given survey', methods=['POST']
)
@api_view(['GET', 'POST'])
def block_list(request, id):
    """
    get:
    Get all blocks within a survey

    post:
    Include a block to a given survey
    """
    try:
        # Needs to include some sort of authentication check here
        survey = Survey.objects.get(pk=id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET list of blocks in a given survey

        blocks = Block.objects.filter(survey=survey.id)
        blocks_serialized = BlockSerializer(blocks, many=True)
        return JsonResponse(blocks_serialized.data, safe=False)
    elif request.method == 'POST':
        # POST a new block

        parsed_request = JSONParser().parse(request)
        parsed_request["survey"] = survey.id

        block_serialized = BlockSerializer(data=parsed_request)

        if block_serialized.is_valid():
            block_serialized.save()
            return JsonResponse(block_serialized.data, status=status.HTTP_201_CREATED)
        return JsonResponse(block_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='Get a specific blocks information by ID', methods=['GET'])
@swagger_auto_schema(operation_summary='Delete a specific block by ID', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Block',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'survey': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Update a blocks information', methods=['PATCH']
)
@api_view(['GET', 'DELETE', 'PATCH'])
def block_info(request, id):
    """
    get:
    Get a specific blocks information by ID

    delete:
    Delete a specific block by ID

    patch:
    Update a blocks information
    """
    try:
        blocks = Block.objects.get(pk=id)
    except Block.DoesNotExist:
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a specific block
        block_serialized = BlockSerializer(blocks)
        return JsonResponse(block_serialized.data)

    elif request.method == 'DELETE':
        # DELETE a specific block
        blocks.delete()
        return JsonResponse({'Message': 'The block has been deleted.'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # Update a specific block

        parsed_request = JSONParser().parse(request)
        block_serialized = BlockSerializer(blocks, data=parsed_request, partial=True)

        if block_serialized.is_valid():
            block_serialized.save()
            return JsonResponse(block_serialized.data)
        return JsonResponse(block_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Block',
        type=openapi.TYPE_OBJECT,
        properties={'survey': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'description': openapi.Schema(type=openapi.TYPE_STRING),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Takes an existing block ID and duplicates it include order for the new block object',
    methods=['POST']
)
@api_view(['POST'])
def duplication_block(request, id):
    """
    post:
    Takes an existing block ID and duplicates it
    {
      order: "include order for the new block object"
    }
    """
    try:
        block = Block.objects.get(pk=id)
    except Block.DoesNotExist:
        return JsonResponse({'Message': 'The block can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        # parse request information to find new question order
        parsed_request = JSONParser().parse(request)

        # get all question references to the block
        questionsInBlock = Question.objects.filter(block=block.id)

        # save a new block with the desired order
        try:
            block.id = None
            block.order = parsed_request['order']
            block.save()
        except Exception as e:
            return JsonResponse({'Message': f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

        for question in questionsInBlock:
            print("New question being handled")

            # create a copy of the subtype information
            questionTypeInformation = questionTypeModel[question.type].objects.get(question=question.id)

            # if multi-choice, button-row or drag and drop get sub-sub-type information
            if (question.type == "Multiple choice"):
                # get a copy of all choices
                choices = MultiChoice.objects.filter(question=questionTypeInformation.id)
            elif (question.type == "Button row"):
                # get a copy of all buttons
                buttons = ButtonQuestion.objects.filter(buttonRow=questionTypeInformation.id)
            elif (question.type == "Drag and drop"):
                # get a copy of all cards
                drag_cards = DragAndDropCard.objects.filter(question=questionTypeInformation.id)
                # then get a copy of all choices
                drag_choices = DragAndDropChoice.objects.filter(question=questionTypeInformation.id)

            # create a copy of the question information
            question.id = None
            questionTypeInformation.id = None

            question.block = block

            try:
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

        block_serialized = BlockSerializer(block)
        return JsonResponse(block_serialized.data, status=status.HTTP_201_CREATED, safe=False)

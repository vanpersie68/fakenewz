from django.http import JsonResponse
from django.urls import is_valid_path
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import MatrixTableQuestion, MatrixTable
from surveybuilder.serializers import MatrixTableQuestionSerializer, MatrixTableSerializer
import json

    
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='MatrixTableQuestion',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'options': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'isDropDown': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'isCheckbox': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'textboxMax': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'textboxMin': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'multipleAnswers': openapi.Schema(type=openapi.TYPE_BOOLEAN), }
    ),
    operation_summary='Update a multiple choice question entity from a multipleChoiceQuestion entity',
    methods=['PATCH']
)
@api_view(['PATCH'])
def question_config(request):
    try:
        parsed_request = JSONParser().parse(request)
        id = parsed_request.get('id')
        del parsed_request['id']
        matrixTableQuestion = MatrixTableQuestion.objects.get(pk=id)
        # print(matrixTableQuestion)
    except MatrixTableQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    matrixTableQuestionSerializer = MatrixTableQuestionSerializer(matrixTableQuestion,parsed_request,partial=True)
    if matrixTableQuestionSerializer.is_valid():
        matrixTableQuestionSerializer.save()
        return JsonResponse(matrixTableQuestionSerializer.data)

    else:
        return JsonResponse(matrixTableQuestionSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return JsonResponse({'123':123})
    return JsonResponse({'a':1})


@api_view(['PATCH'])
def multiple_choice_data(request, id):
    """
    patch:
    Update a multiple choice question entity from a multipleChoiceQuestion entity
    """
    try:
        matrixTableQuestion = MatrixTableQuestion.objects.get(pk=id)
    except MatrixTableQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        parsed_request = JSONParser().parse(request)
        multi_choice_question_serialized = MatrixTableQuestionSerializer(matrixTableQuestion, parsed_request,
                                                                         partial=True)
        # save the question
        if multi_choice_question_serialized.is_valid():
            multi_choice_question_serialized.save()
            return JsonResponse(multi_choice_question_serialized.data)
        else:
            return JsonResponse(multi_choice_question_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='Given a MultipleChoice entity ID, return the entity and its choices',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='MatrixTable',
        type=openapi.TYPE_OBJECT,
        properties={'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING), }
    ),
    operation_summary='Include a new choice entity to a MultipleChoice entity',
    methods=['POST']
)
@swagger_auto_schema(operation_summary='Delete a choice entity from a MultipleChoice entity', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='MatrixTable',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING), }
    ),
    operation_summary='Update a choice entity from a MultipleChoice entity',
    methods=['PATCH']
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def choices_data(request, id):
    """
    get:
    Given a multiplechoice entity ID, return the entity and its choices

    post:
    Include a new choice entity to a multiplechoice entity

    delete:
    Delete a choice entity from a multiplechoice entity

    patch:
    Update a choice entity from a multiplechoice entity
    """
    try:
        matrixTableQuestion = MatrixTableQuestion.objects.get(pk=id)
    except MatrixTableQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a MatrixTable questions information
        MatrixTableQuestionSerialized = MatrixTableQuestionSerializer(MatrixTableQuestion)

        choices = MatrixTable.objects.filter(question=id)
        choicesSerialized = MatrixTableSerializer(choices, many=True)

        # Include all button information to the MatrixTable data
        multi_data = MatrixTableQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]

        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the multiplechoice question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = MatrixTableQuestion.id
        choice_serialized = MatrixTableSerializer(data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            MatrixTableQuestion.options += 1
            MatrixTableQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment MatrixTable count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        MatrixTable_id = parsed_request['id']

        try:
            choice = MatrixTable.objects.get(id=MatrixTable_id)
            choice.delete()
            MatrixTableQuestion.options -= 1
            MatrixTableQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the choice'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = MatrixTableQuestion.id

        # fetch the preexisting object and check incoming request
        choice = MatrixTable.objects.get(id=parsed_request['id'])
        choice_serialized = MatrixTableSerializer(choice, data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

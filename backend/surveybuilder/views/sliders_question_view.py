from django.http import JsonResponse
from django.urls import is_valid_path
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import SlidersQuestion, Sliders
from surveybuilder.serializers import SlidersQuestionSerializer, SlidersSerializer
import json

    
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='SlidersQuestion',
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
        slidersQuestion = SlidersQuestion.objects.get(pk=id)
        # print(slidersQuestion)
    except SlidersQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    slidersQuestionSerializer = SlidersQuestionSerializer(slidersQuestion,parsed_request,partial=True)
    if slidersQuestionSerializer.is_valid():
        slidersQuestionSerializer.save()
        return JsonResponse(slidersQuestionSerializer.data)

    else:
        return JsonResponse(slidersQuestionSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return JsonResponse({'123':123})
    return JsonResponse({'a':1})


@api_view(['PATCH'])
def sliders_data(request, id):
    """
    patch:
    Update a multiple choice question entity from a multipleChoiceQuestion entity
    """
    try:
        slidersQuestion = SlidersQuestion.objects.get(pk=id)
    except SlidersQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        parsed_request = JSONParser().parse(request)
        multi_choice_question_serialized = SlidersQuestionSerializer(slidersQuestion, parsed_request,
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
        title='Sliders',
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
        title='Sliders',
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
        slidersQuestion = SlidersQuestion.objects.get(pk=id)
    except SlidersQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a Sliders questions information
        SlidersQuestionSerialized = SlidersQuestionSerializer(SlidersQuestion)

        choices = Sliders.objects.filter(question=id)
        choicesSerialized = SlidersSerializer(choices, many=True)

        # Include all button information to the Sliders data
        multi_data = SlidersQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]

        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the multiplechoice question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = SlidersQuestion.id
        choice_serialized = SlidersSerializer(data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            SlidersQuestion.options += 1
            SlidersQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment Sliders count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        Sliders_id = parsed_request['id']

        try:
            choice = Sliders.objects.get(id=Sliders_id)
            choice.delete()
            SlidersQuestion.options -= 1
            SlidersQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the choice'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = SlidersQuestion.id

        # fetch the preexisting object and check incoming request
        choice = Sliders.objects.get(id=parsed_request['id'])
        choice_serialized = SlidersSerializer(choice, data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

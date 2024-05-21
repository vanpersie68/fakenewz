from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import MultiChoiceQuestion, MultiChoice
from surveybuilder.serializers import MultiChoiceQuestionSerializer, MultiChoiceSerializer


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='MultiChoiceQuestion',
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
def multiple_choice_data(request, id):
    """
    patch:
    Update a multiple choice question entity from a multipleChoiceQuestion entity
    """
    try:
        multiChoiceQuestion = MultiChoiceQuestion.objects.get(pk=id)
    except MultiChoiceQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == "PATCH":
        parsed_request = JSONParser().parse(request)
        multi_choice_question_serialized = MultiChoiceQuestionSerializer(multiChoiceQuestion, parsed_request,
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
        title='MultiChoice',
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
        title='MultiChoice',
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
        multiChoiceQuestion = MultiChoiceQuestion.objects.get(pk=id)
    except MultiChoiceQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The multiplechoice question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a multichoice questions information
        multiChoiceQuestionSerialized = MultiChoiceQuestionSerializer(multiChoiceQuestion)

        choices = MultiChoice.objects.filter(question=id)
        choicesSerialized = MultiChoiceSerializer(choices, many=True)

        # Include all button information to the multichoice data
        multi_data = multiChoiceQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]

        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the multiplechoice question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = multiChoiceQuestion.id
        choice_serialized = MultiChoiceSerializer(data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            multiChoiceQuestion.options += 1
            multiChoiceQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment multichoice count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        multichoice_id = parsed_request['id']

        try:
            choice = MultiChoice.objects.get(id=multichoice_id)
            choice.delete()
            multiChoiceQuestion.options -= 1
            multiChoiceQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the choice'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = multiChoiceQuestion.id

        # fetch the preexisting object and check incoming request
        choice = MultiChoice.objects.get(id=parsed_request['id'])
        choice_serialized = MultiChoiceSerializer(choice, data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

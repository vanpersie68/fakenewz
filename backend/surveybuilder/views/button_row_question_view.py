from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import ButtonRowQuestion, ButtonQuestion
from surveybuilder.serializers import ButtonRowQuestionSerializer, ButtonQuestionSerializer


@swagger_auto_schema(operation_summary='Given a ButtonRow entity ID, return the entity and its buttons',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='ButtonQuestion',
        type=openapi.TYPE_OBJECT,
        properties={'buttonRow': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'buttonText': openapi.Schema(type=openapi.TYPE_STRING),
                    'buttonType': openapi.Schema(type=openapi.TYPE_STRING),
                    'buttonIcon': openapi.Schema(type=openapi.TYPE_STRING),
                    'answered': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'jumpBlockId': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Include a new button entity to a ButtonRow entity',
    methods=['POST']
)
@swagger_auto_schema(operation_summary='Delete a button entity from a ButtonRow entity', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='ButtonQuestion',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'buttonRow': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'buttonText': openapi.Schema(type=openapi.TYPE_STRING),
                    'buttonType': openapi.Schema(type=openapi.TYPE_STRING),
                    'buttonIcon': openapi.Schema(type=openapi.TYPE_STRING),
                    'answered': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'jumpBlockId': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Update a button entity from a ButtonRow entity',
    methods=['PATCH']
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def buttonrow_data(request, id):
    """
    get:
    Given a buttonrow entity ID, return the entity and its buttons

    post:
    Include a new button entity to a buttonrow entity

    delete:
    Delete a button entity from a buttonrow entity

    patch:
    Update a button entity from a buttonrow entity
    """
    try:
        buttonrowQuestion = ButtonRowQuestion.objects.get(pk=id)
    except ButtonRowQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The buttonrow can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a buttonrow questions information
        buttonrowQuestionSerialized = ButtonRowQuestionSerializer(buttonrowQuestion)
        buttons = ButtonQuestion.objects.filter(buttonRow=id)
        buttonsSerialized = ButtonQuestionSerializer(buttons, many=True)

        # Include all button information to the buttonrow data
        buttonrow_data = buttonrowQuestionSerialized.data
        buttonrow_data['buttons'] = buttonsSerialized.data[:]

        return JsonResponse(buttonrow_data)
    elif request.method == 'POST':
        # POST a button to the buttonrow question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['buttonRow'] = buttonrowQuestion.id
        button_serialized = ButtonQuestionSerializer(data=parsed_request)

        # save the button input
        if button_serialized.is_valid():
            button_serialized.save()
        else:
            return JsonResponse(button_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            buttonrowQuestion.numberButtons += 1
            buttonrowQuestion.save()
            return JsonResponse(button_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment buttonrow count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        button_id = parsed_request['id']

        try:
            buttons = ButtonQuestion.objects.get(id=button_id)
            buttons.delete()
            buttonrowQuestion.numberButtons -= 1
            buttonrowQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the button.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the button'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['buttonRow'] = buttonrowQuestion.id

        # fetch the preexisting object and check incoming request
        button = ButtonQuestion.objects.get(id=parsed_request['id'])
        button_serialized = ButtonQuestionSerializer(button, data=parsed_request, partial=True)

        # save the button input
        if button_serialized.is_valid():
            button_serialized.save()
            return JsonResponse(button_serialized.data)
        else:
            return JsonResponse(button_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import DragAndDropQuestion, DragAndDropChoice, DragAndDropCard
from surveybuilder.serializers import DragAndDropQuestionSerializer, DragAndDropCardSerializer, \
    DragAndDropChoiceSerializer


@swagger_auto_schema(operation_summary='Given a drag and drop entity ID, return the entity and its cards',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='DragAndDropCard',
        type=openapi.TYPE_OBJECT,
        properties={'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='include a new card entity',
    methods=['POST']
)
@swagger_auto_schema(operation_summary='Delete a card entity', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='DragAndDropCard',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='update a card entity',
    methods=['PATCH']
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def dragdropcard_data(request, id):
    """
    get:
    Given a drag and drop entity ID, return the entity and its cards

    post:
    include a new card entity

    delete:
    delete a card entity

    patch:
    update a card entity
    """
    try:
        dragdropQuestion = DragAndDropQuestion.objects.get(pk=id)
    except DragAndDropQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The Drag and Drop question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a drag and drop question's card information
        dragAndDropQuestionSerialized = DragAndDropQuestionSerializer(dragdropQuestion)

        cards = DragAndDropChoice.objects.filter(question=id)
        cardsSerialized = DragAndDropCardSerializer(cards, many=True)

        # Include all card information to the drag and drop data
        multi_data = dragAndDropQuestionSerialized.data
        multi_data['cards'] = cardsSerialized.data[:]

        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a card to the drag and drop question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id
        card_serialized = DragAndDropCardSerializer(data=parsed_request)

        # save the button input
        if card_serialized.is_valid():
            card_serialized.save()
        else:
            return JsonResponse(card_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            dragdropQuestion.cards += 1
            dragdropQuestion.save()
            return JsonResponse(card_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment card count for drag and drop question.'},
                                status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a choice from the drag and drop

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        card_id = parsed_request['id']

        try:
            card = DragAndDropCard.objects.get(id=card_id)
            card.delete()
            dragdropQuestion.cards -= 1
            dragdropQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the card from the drag and drop question.'},
                         status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the card from the drag and drop question.'},
                            status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing card within the drag and drop question

        # parse the card input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id

        # fetch the preexisting object and check incoming request
        card = DragAndDropChoice.objects.get(id=parsed_request['id'])
        card_serialized = DragAndDropCardSerializer(card, data=parsed_request)

        # save the choice input
        if card_serialized.is_valid():
            card_serialized.save()
            return JsonResponse(card_serialized.data)
        else:
            return JsonResponse(card_serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='Given a drag and drop entity ID, return the entity and its choices',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='DragAndDropChoice',
        type=openapi.TYPE_OBJECT,
        properties={'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Include a new choice entity to a drag and drop entity',
    methods=['POST']
)
@swagger_auto_schema(operation_summary='Delete a choice entity from a drag and drop entity', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='DragAndDropChoice',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'order': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update a choice entity from a drag and drop entity',
    methods=['PATCH']
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def dragdropchoice_data(request, id):
    """
    get:
    Given a drag and drop entity ID, return the entity and its choices

    post:
    Include a new choice entity to a drag and drop entity

    delete:
    Delete a choice entity from a drag and drop entity

    patch:
    Update a choice entity from a drag and drop entity
    """
    try:
        dragdropQuestion = DragAndDropQuestion.objects.get(pk=id)
    except DragAndDropQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The Drag and Drop question can\'t be found.'},
                            status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a drag and drop question's choice information
        dragAndDropQuestionSerialized = DragAndDropQuestionSerializer(dragdropQuestion)

        choices = DragAndDropChoice.objects.filter(question=id)
        choicesSerialized = DragAndDropChoiceSerializer(choices, many=True)

        # Include all choice information to the drag and drop data
        multi_data = dragAndDropQuestionSerialized.data
        multi_data['choices'] = choicesSerialized.data[:]

        return JsonResponse(multi_data)
    elif request.method == 'POST':
        # POST a choice to the drag and drop question

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id
        choice_serialized = DragAndDropChoiceSerializer(data=parsed_request)

        # save the button input
        if choice_serialized.is_valid():
            choice_serialized.save()
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the buttonrow counter
        try:
            dragdropQuestion.choices += 1
            dragdropQuestion.save()
            return JsonResponse(choice_serialized.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment choice count for drag and drop question.'},
                                status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a choice from the drag and drop

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        choice_id = parsed_request['id']

        try:
            choice = DragAndDropChoice.objects.get(id=choice_id)
            choice.delete()
            dragdropQuestion.choices -= 1
            dragdropQuestion.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the choice from the drag and drop question.'},
                         status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the choice from the drag and drop question.'},
                            status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing choice within the drag and drop question

        # parse the choice input
        parsed_request = JSONParser().parse(request)
        parsed_request['question'] = dragdropQuestion.id

        # fetch the preexisting object and check incoming request
        choice = DragAndDropChoice.objects.get(id=parsed_request['id'])
        choice_serialized = DragAndDropChoiceSerializer(choice, data=parsed_request)

        # save the choice input
        if choice_serialized.is_valid():
            choice_serialized.save()
            return JsonResponse(choice_serialized.data)
        else:
            return JsonResponse(choice_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

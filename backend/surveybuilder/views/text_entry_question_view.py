from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from surveybuilder.models import TextboxQuestionText
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.serializers import TextboxQuestionTextSerializer
from rest_framework.parsers import JSONParser


@swagger_auto_schema(operation_summary='Given a TextEntry entity ID, return the entity', methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='MultiChoiceQuestion',
        type=openapi.TYPE_OBJECT,
        properties={'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'query': openapi.Schema(type=openapi.TYPE_STRING),
                    'validate': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'textboxMax': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'textboxMin': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'ansType': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Update a TextEntry entity',
    methods=['PATCH']
)
@api_view(['GET', 'PATCH'])
def text_entry_info(request, id):
    try:
        text_entry = TextboxQuestionText.objects.get(question_id=id)
    except TextboxQuestionText.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        text_entry_serialized = TextboxQuestionTextSerializer(text_entry)
        return JsonResponse(text_entry_serialized.data, safe=False)
    if request.method == 'PATCH':
        parsed_request = JSONParser().parse(request)
        text_entry_serialized = TextboxQuestionTextSerializer(text_entry, data=parsed_request, partial=True)
        if text_entry_serialized.is_valid():
            text_entry_serialized.save()
            return JsonResponse(text_entry_serialized.data, safe=False)
        return JsonResponse(text_entry_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

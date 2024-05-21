from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from surveybuilder.models import NumberScaleQuestion
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.serializers import NumberScaleQuestionSerializer
from rest_framework.parsers import JSONParser


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='NumberScaleQuestion',
        type=openapi.TYPE_OBJECT,
        properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'question': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'minTitle': openapi.Schema(type=openapi.TYPE_STRING),
                    'middleTitle': openapi.Schema(type=openapi.TYPE_STRING),
                    'maxTitle': openapi.Schema(type=openapi.TYPE_STRING),
                    'interval': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'numberMax': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'numberMin': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'minTitleOn': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'midTitleOn': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'maxTitleOn': openapi.Schema(type=openapi.TYPE_BOOLEAN)}
    ),
    operation_summary='Update a NumberScaleQuestion entity',
    methods=['PATCH']
)
@api_view(['PATCH'])
def number_scale_info(request, id):
    try:
        number_scale = NumberScaleQuestion.objects.get(question_id=id)
    except NumberScaleQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The question can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PATCH':
        parsed_request = JSONParser().parse(request)
        if 'minTitleOn' in parsed_request and parsed_request["minTitleOn"] == 0:
            parsed_request = {
                "minTitleOn": 0,
                "minTitle": ""
            }
        elif 'midTitleOn' in parsed_request and parsed_request["midTitleOn"] == 0:
            parsed_request = {
                "midTitleOn": 0,
                "middleTitle": ""
            }
        elif 'maxTitleOn' in parsed_request and parsed_request["maxTitleOn"] == 0:
            parsed_request = {
                "maxTitleOn": 0,
                "maxTitle": ""
            }
        number_scale_serialized = NumberScaleQuestionSerializer(number_scale, data=parsed_request, partial=True)
        if number_scale_serialized.is_valid():
            number_scale_serialized.save()
            return JsonResponse(number_scale_serialized.data, safe=False)
        return JsonResponse(number_scale_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

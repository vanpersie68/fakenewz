import json

from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from surveybuilder.models import Survey, RandomSections
from surveybuilder.serializers import RadomSectionsSerializer


@swagger_auto_schema(operation_summary='Given a RandomSection entity ID, return the RandomSection entity',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='RandomSections',
        type=openapi.TYPE_OBJECT,
        properties={'postRow': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'display': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'startWith': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'endWith': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'index': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Update RandomSection information by ID',
    methods=['PATCH']
)
@api_view(['GET', 'PATCH'])
def randomSections_info(request, survey_id):
    try:
        randomSections = RandomSections.objects.filter(survey=survey_id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    randomSections_serialized = RadomSectionsSerializer(randomSections, many=True)
    randomSections_data = randomSections_serialized.data
    if request.method == 'GET':
        result = []
        for (i, rs) in enumerate(randomSections_data):
            subset = {'display': rs['display'], 'startWith': rs['startWith'], 'endWith': rs['endWith'],
                      'index': rs['index']}
            result.append(subset)
        return JsonResponse(result, safe=False)

    elif request.method == 'PATCH':
        parsed_request = JSONParser().parse(request)
        randomSection_serialized = RadomSectionsSerializer(data=parsed_request, many=True)
        randomSections.delete()
        if randomSection_serialized.is_valid():
            randomSection_serialized.save()
            return JsonResponse(parsed_request, safe=False)
        return JsonResponse(randomSection_serialized.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='RandomSections',
        type=openapi.TYPE_OBJECT,
        properties={'survey': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'display': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'startWith': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'endWith': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'index': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Create a new RandomSections entity',
    methods=['POST']
)
@api_view(['POST'])
def create_randomSections(request):
    order = request.GET.get("order")
    survey_id = request.GET.get("survey_id")

    try:
        randomSections = RandomSections.objects.filter(survey=survey_id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    randomSections_serialized = RadomSectionsSerializer(randomSections, many=True)
    randomSections_data = randomSections_serialized.data
    subset = {'survey': survey_id, 'startWith': order, 'endWith': order, 'index': len(randomSections_data)}

    randomSection_serialized = RadomSectionsSerializer(data=subset)
    if randomSection_serialized.is_valid():
        randomSection_serialized.save()
        return JsonResponse(randomSection_serialized.data)
    return JsonResponse(randomSection_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

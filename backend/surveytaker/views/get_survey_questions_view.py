from django.http import JsonResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view

from surveybuilder.models import Survey, Block
from surveybuilder.serializers import SurveySerializer
from surveybuilder.views.survey_view import get_survey_data

@swagger_auto_schema(operation_summary='get survey questions according to the code', methods=['GET'])
@api_view(['GET'])
def get_survey_questions(request, code):
    """
    GET:
    Get survey questions according to the code
    """
    try:
        survey = Survey.objects.get(code=code)
        blocks = Block.objects.filter(survey=survey.id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    survey_serialized = SurveySerializer(survey)
    survey_data = survey_serialized.data
    if survey_data['status'] == 0:
        return JsonResponse({'code': 999, 'message': 'Survey not yet released'})
    if survey_data['status'] == 2:
        return JsonResponse({'code': 999, 'message': 'Survey has been closed.'})
    survey_data = get_survey_data(survey, blocks)
    return JsonResponse(survey_data, status=status.HTTP_200_OK, safe=False)

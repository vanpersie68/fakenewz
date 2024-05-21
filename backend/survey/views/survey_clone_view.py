
from django.http import request, JsonResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from survey.views.survey_import_view import import_survey, import_survey_data
from surveybuilder.models import Survey, Block
from surveybuilder.views.survey_view import survey_data, get_survey_data


@swagger_auto_schema(operation_summary='Clone current survey', methods=['POST'])
@api_view(["POST"])
def clone_survey(request,survey_id,researcher_id, to_language):
    # add a new parameter： to_language
    """
    post:
    Clone current survey
    """
    try:
        survey = Survey.objects.get(id=survey_id)
        blocks = Block.objects.filter(survey=survey.id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    survey_data = get_survey_data(survey, blocks)
    survey_data['name'] = survey_data['name']+' (cloned)'

    try:
        # to_language = None
        import_survey_data(survey_data, researcher_id, to_language)
    except Exception:
        print(Exception.with_traceback())
        return Response({"status": "Survey clone failed","code":400})
    
    return Response({"status": "success","code":200})



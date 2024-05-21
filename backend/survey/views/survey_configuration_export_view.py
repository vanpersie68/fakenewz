from django.http import HttpResponse
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound

from survey import models
from surveybuilder.models import Survey
from surveybuilder.views.survey_view import survey_data

@swagger_auto_schema(operation_summary='export survey configuration file', methods=['GET'])
@api_view(["GET"])
def export_survey(request, survey_id):
    """
    get:
    Export survey configuration file
    """
    # fetch survey title, id, language
    try:
        survey = Survey.objects.get(id=survey_id)
    except models.ObjectDoesNotExist:
        raise NotFound(detail="Survey not found!", code=None)
    config_json = survey_data(request._request, survey_id)

    response = HttpResponse(
        config_json,
        content_type='application/json',
        headers={
            'Content-Disposition': f'attachment; filename="{survey.name} {survey.language} Version Configuration (ID {survey.id}).json"'},
    )
    return response
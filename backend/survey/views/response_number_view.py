from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from surveybuilder.models import Survey
from surveytaker.models import Response
from surveybuilder.serializers import SurveySerializer


@api_view(['GET'])
def response_number(request, survey_id):
    try:
        survey = Survey.objects.get(pk=survey_id)
    except Survey.DoesNotExist:
        return JsonResponse({'Message': 'The survey can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)
    survey_serialized = SurveySerializer(survey)
    survey_data = survey_serialized.data
    status_code = survey_data['status']  # 1 published, 0 saved, 2 end
    # whether there are preview response
    if status_code == 0:
        try:
            responses = Response.objects.filter(survey=survey_id, preview=1)
            if len(responses) > 0:
                return JsonResponse({'Message': 'Preview, have response'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'Message': 'Preview, no response'}, status=status.HTTP_404_NOT_FOUND)
        except Response.DoesNotExist:
            return JsonResponse({'Message': 'Preview, no response'}, status=status.HTTP_404_NOT_FOUND)
    # whether there are normal response
    elif status_code == 1 or status_code == 2:
        try:
            responses = Response.objects.filter(survey=survey_id, preview=0)
            if len(responses) > 0:
                return JsonResponse({'Message': 'Normal, have response'}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({'Message': 'Normal, no response'}, status=status.HTTP_404_NOT_FOUND)
        except Response.DoesNotExist:
            return JsonResponse({'Message': 'Normal, no response'}, status=status.HTTP_404_NOT_FOUND)
    return JsonResponse(status_code, status=status.HTTP_200_OK, safe=False)

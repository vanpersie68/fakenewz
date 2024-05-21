from rest_framework.decorators import api_view
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from surveybuilder.models import Survey
from rest_framework import exceptions, status
from django.http import JsonResponse, HttpResponse

from surveybuilder.serializers import UserSerializer


@api_view(['POST'])
def update_collaborator(request):
    key = request.data.get('key')
    survey_id = request.data.get('surveyid')


    new_collaborator = get_user_id(key)

    try:
        survey = Survey.objects.get(id=survey_id)
        # current_collaborators = survey.collaborator

        if new_collaborator not in survey.collaborator:
            survey.collaborator.append(new_collaborator)
            survey.save()

            return HttpResponse("Collaborator added successfully.")
        else:
            return HttpResponse("Collaborator already exists.", status=400)
    except Survey.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

def get_user_id(key):
    try:
        token = Token.objects.get(key=key)
        user = token.user
        print(key)
        # console.log(user_id)
        return user.id
    except Token.DoesNotExist:
        return None

@api_view(['POST'])
def delete_collaborator(request):
    survey_id = request.data.get('survey_id')
    user_id = request.data.get('user_id')
    survey = Survey.objects.get(id=survey_id)
    if user_id in survey.collaborator:
        survey.collaborator.remove(user_id)
        survey.save()
        return HttpResponse("Collaborator removed successfully.")
    else:
        return HttpResponse("Collaborator not found in the list.", status=400)

def get_collaborator(request, id):
    # survey_id = request.data.get('surveyid')
    survey = Survey.objects.get(id=id)
    users = []

    if survey.collaborator:
        for u in survey.collaborator:
            user = User.objects.get(id=u)
            users.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # 添加其他需要的用户信息字段
            })
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
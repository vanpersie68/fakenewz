from django.http import JsonResponse
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from surveybuilder.const import questionTypeModel
from surveybuilder.models import Avatar, Survey, Block, Question, MultiChoice, ButtonQuestion, DragAndDropCard, \
    DragAndDropChoice
from surveybuilder.serializers import BlockSerializer
import random
from pathlib import Path
import os
import json
import difflib
from surveybuilder.serializers import AvatarSerializer

BASE_DIR = Path(__file__).resolve().parent.parent.parent
from django.http import HttpResponse,JsonResponse

# @api_view(['POST'])
def upload(request):
    file = request.FILES.get("file", None)
    r = str(random.random())
    destination = open(os.path.join(BASE_DIR,'static','upload',r+file.name),'wb+')
    for chunk in file.chunks():      # 分块写入文件
        destination.write(chunk)
        destination.close()
    return HttpResponse(json.dumps({
        'code': 0,
        'value': '/upload/'+r+file.name
    }))
@api_view(['POST','GET','DELETE'])
def avatar(request):
    if request.method == 'GET':
        user = request.query_params['user']
        avatars = Avatar.objects.filter(**{'user': user})
        avatars_serialized = AvatarSerializer(avatars, many=True)
        return JsonResponse(avatars_serialized.data, safe=False)
    if request.method == 'POST':
 
        parsed_request = JSONParser().parse(request)
        avatar_serialized = AvatarSerializer(data=parsed_request)
        if avatar_serialized.is_valid():
            avatar_serialized.save()
            return JsonResponse(avatar_serialized.data, status=status.HTTP_201_CREATED)
        return JsonResponse(avatar_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            id = request.query_params['id']
            el = Avatar.objects.get(id=id)
            el.delete()
        except Exception as e:
                print(e)
                
        return JsonResponse({'Message': 'The avatar has been deleted.'}, status=status.HTTP_204_NO_CONTENT)

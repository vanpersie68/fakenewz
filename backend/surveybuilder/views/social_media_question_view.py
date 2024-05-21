# Has to be a POST request due to issues in axios not being able to send data in GET
# See: https://stackoverflow.com/questions/46404051/send-object-with-axios-get-request
from django.http import JsonResponse
from drf_yasg2 import openapi
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from drf_yasg2.utils import swagger_auto_schema
from services.articledata import extract_article_metadata
from services.videodata import extra_video_data
from surveybuilder.models import PostAddonfield, SocialPostQuestion
from surveybuilder.serializers import PostAddonfieldSerializer, SocialPostQuestionSerializer


@swagger_auto_schema(
    request_body=openapi.Schema(
        title='Link',
        type=openapi.TYPE_OBJECT,
        properties={'link': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    operation_summary='Given a link, return all relevant metadata',
    methods=['POST']
)
@api_view(['POST'])
def article_information(request):
    """
    post:
    Given a link, return all relevant metadata
    """
    try:
        parsed_request = JSONParser().parse(request)
        link = parsed_request['link']
    except Exception:
        return JsonResponse({'Message': 'Bad link.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        articleData = extract_article_metadata(link)
        return JsonResponse(articleData, safe=False)


@swagger_auto_schema(operation_summary='Given a link, return all relevant metadata of the video', methods=['GET'])
@api_view(['GET'])
def video_information(request):
    """
    post:
    Given a link, return all relevant metadata of the video
    """
    try:
        query_dict = request.GET
        link = query_dict.get('link')
    except Exception:
        return JsonResponse({'Message': 'Bad link.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        video_data = extra_video_data(link)
        return JsonResponse(video_data, safe=False)


@swagger_auto_schema(operation_summary='Given a postAddonField entity ID, return the entity and its buttons',
                     methods=['GET'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='PostAddonfield',
        type=openapi.TYPE_OBJECT,
        properties={'postRow': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'icon': openapi.Schema(type=openapi.TYPE_STRING),
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Include a new button entity to a postAddonField entity',
    methods=['POST']
)
@swagger_auto_schema(operation_summary='Delete a button entity from a postAddonField entity', methods=['DELETE'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        title='PostAddonfield',
        type=openapi.TYPE_OBJECT,
        properties={'postRow': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'title': openapi.Schema(type=openapi.TYPE_STRING),
                    'icon': openapi.Schema(type=openapi.TYPE_STRING),
                    'count': openapi.Schema(type=openapi.TYPE_INTEGER)}
    ),
    operation_summary='Update a button entity from a postAddonField entity',
    methods=['PATCH']
)
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def postAddonField_data(request, id):
    """
    get:
    Given a postAddonField entity ID, return the entity and its buttons

    post:
    Include a new button entity to a postAddonField entity

    delete:
    Delete a button entity from a postAddonField entity

    patch:
    Update a button entity from a postAddonField entity
    """
    try:
        socialPost = SocialPostQuestion.objects.get(pk=id)
    except SocialPostQuestion.DoesNotExist:
        return JsonResponse({'Message': 'The buttonrow can\'t be found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # GET a postAddonfield questions information
        socialPostSerialized = SocialPostQuestionSerializer(socialPost)
        postAddonfield = PostAddonfield.objects.filter(postRow=id)
        postAddonfieldSerializer = PostAddonfieldSerializer(postAddonfield, many=True)

        # Include all socialPost information to the buttonrow data
        socialPost_data = socialPostSerialized.data
        socialPost_data['addon'] = postAddonfieldSerializer.data[:]

        return JsonResponse(socialPost_data)
    elif request.method == 'POST':
        # POST a button to the postAddonfield question

        # parse the socialPost input
        parsed_request = JSONParser().parse(request)
        parsed_request['postRow'] = socialPost.id
        postAddonfieldSerializer = PostAddonfieldSerializer(data=parsed_request)

        # save the socialPost input
        if postAddonfieldSerializer.is_valid():
            postAddonfieldSerializer.save()
        else:
            return JsonResponse(postAddonfieldSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # increment the postAddonfield counter
        try:
            socialPost.numberAddon += 1
            socialPost.save()
            return JsonResponse(postAddonfieldSerializer.data, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({'Message': 'Couldnt increment socialPost count.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # DELETE a button from the button row

        # Expects an object like such {"id": <to-be-deleted>} for the button
        parsed_request = JSONParser().parse(request)
        addon_id = parsed_request['id']

        try:
            postAddonfield = PostAddonfield.objects.get(id=addon_id)
            postAddonfield.delete()
            socialPost.numberButtons -= 1
            socialPost.save()
        except:
            JsonResponse({'Message': 'Couldnt delete the socialPost.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'Message': 'Successfully deleted the socialPost'}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PATCH':
        # UPDATE an existing button within the button row

        # parse the button input
        parsed_request = JSONParser().parse(request)
        parsed_request['postRow'] = socialPost.id

        # fetch the preexisting object and check incoming request
        postAddonfield = PostAddonfield.objects.get(id=parsed_request['id'])
        postAddonfieldSerialized = PostAddonfieldSerializer(postAddonfield, data=parsed_request, partial=True)

        # save the button input
        if postAddonfieldSerialized.is_valid():
            postAddonfieldSerialized.save()
            return JsonResponse(postAddonfieldSerialized.data)
        else:
            return JsonResponse(postAddonfieldSerialized.errors, status=status.HTTP_400_BAD_REQUEST)

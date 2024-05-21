from rest_framework.decorators import api_view
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from surveybuilder.models import Survey
from rest_framework import exceptions
from django.http import JsonResponse, HttpResponse
from .models import EmailInfo
from rest_framework.response import Response
from rest_framework import status
from emailInfo.serializer import EmailInfoSerializer
from django.db.models import Q




# @api_view(['POST'])
def add_email_info(sender, receiver, survey):
    email_info = EmailInfo(sender=sender, receiver=receiver, survey=survey)
    email_info.save()
    return email_info.id
    # serializer = EmailInfoSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def check_expiration(request, sender, recipient, questionnaire_id):
    try:
        email_info = EmailInfo.objects.get(sender=sender, recipient=recipient, questionnaire_id=questionnaire_id)
        is_expired = email_info.expiration_time < timezone.now()
        return Response({"is_expired": is_expired}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_verification(request, email_info_id):
    try:
        email_info = EmailInfo.objects.get(pk=email_info_id)
        email_info.is_verified = True
        email_info.save()
        return Response({"message": "You have accept the invitation."}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def update_rejected(request, email_info_id):
    try:
        email_info = EmailInfo.objects.get(pk=email_info_id)
        email_info.rejected = True
        email_info.save()
        return Response({"message": "You have rejected the invitation."}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getRejected(request, email_info_id):
    try:
        email_info = EmailInfo.objects.get(pk=email_info_id)
        return Response({"message": email_info.rejected}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getAccept(request, email_info_id):
    try:
        email_info = EmailInfo.objects.get(pk=email_info_id)
        return Response({"message": email_info.accepted}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def update_accept(request, email_info_id):
    try:
        email_info = EmailInfo.objects.get(pk=email_info_id)
        email_info.accepted = True
        email_info.save()
        return Response({"message": "You have accept the invitation."}, status=status.HTTP_200_OK)
    except EmailInfo.DoesNotExist:
        return Response({"message": "Email info not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_emails(request, receiver_id): # will return the info (accept = false && reject == false)
    receiver = User.objects.get(pk=receiver_id)
    receiver_emails = EmailInfo.objects.filter(
        Q(receiver=receiver, accepted=False, rejected=False)
    )
    serializer = EmailInfoSerializer(receiver_emails, many=True)
    return JsonResponse(serializer.data, safe=False)
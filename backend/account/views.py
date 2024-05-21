from allauth.account.utils import send_email_confirmation
from rest_auth.app_settings import PasswordChangeSerializer
from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from django.http import JsonResponse
from rest_auth.serializers import PasswordResetConfirmSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from surveybuilder.models import Survey
from rest_framework.authtoken.models import Token
from emailInfo.views import add_email_info


@swagger_auto_schema(
    request_body=openapi.Schema(
    title="Name",
    type=openapi.TYPE_OBJECT,
    properties={'first_name': openapi.Schema(type=openapi.TYPE_STRING),'last_name': openapi.Schema(type=openapi.TYPE_STRING)}),
    operation_summary='update user profile', methods=['POST'])
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def update_user(request):
    """
    post:
    Update user profile
    """
    first_name = request.data["first_name"] if "first_name" in request.data else None
    last_name = request.data["last_name"] if "last_name" in request.data else None
    user = request.user
    if first_name is None or first_name == "":
        pass
    else:
        user.first_name = first_name
    if last_name is None or last_name == "":
        pass
    else:
        user.last_name = last_name
    user.save()
    return Response({"detail": "Name updated."})

@swagger_auto_schema(operation_summary='send verification email', methods=['POST'])
@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def send_verification_email(request):
    """
    post:
    Send verification email
    """
    send_email_confirmation(request, request.user)
    return Response({"detail": "Verification email sent"})

@swagger_auto_schema(operation_summary='delete user account', methods=['DELETE'])
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, ])
def delete_user(request):
    """
    delete:
    Delete user account
    """
    user = request.user
    try:
        user.delete()
    # catch-all exception
    # if not logged in, the authentication wrapper should return 403 instead
    except Exception:
        return Response({"detail": "User cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
    # return success if deletion successful
    return Response({"detail": "User has been deleted"})


@swagger_auto_schema(
    request_body=openapi.Schema(
        title="Name",
        type=openapi.TYPE_OBJECT,
        properties={'new_password1': openapi.Schema(type=openapi.TYPE_STRING),
                    'new_password2': openapi.Schema(type=openapi.TYPE_STRING),
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'uid': openapi.Schema(type=openapi.TYPE_STRING)}),
    operation_summary='Reset password', methods=['POST'])
@api_view(["POST"])
@permission_classes([AllowAny, ])
def forget_password(request):
    serializer_class = PasswordResetConfirmSerializer
    serializer = serializer_class(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(
            {"detail": "Password has been reset with the new password."}, status=status.HTTP_200_OK
        )
    except ValidationError:
        error_msgs = []
        error_code = []
        exception = str(ValidationError(serializer.errors))
        for msg in exception.split(":")[1].split("ErrorDetail"):
            if msg.__contains__("string"):
                error_msgs.append(msg.split(",")[0].split("=")[1].split("'")[1])
        for err in error_msgs:
            if err == 'This password is too short. It must contain at least 8 characters.':
                error_code.append(1)
            elif err == 'This password is too common.':
                error_code.append(2)
            elif err == 'This password is entirely numeric.':
                error_code.append(3)
            elif err == 'This field may not be blank.':
                error_code.append(4)
            elif err == 'The two password fields didn’t match.':
                error_code.append(5)
            else:
                error_code.append(6)  # Unknown error, please try again
        return JsonResponse({'Message': error_code}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, ])
def reset_password(request):
    serializer_class = PasswordChangeSerializer
    serializer = serializer_class(data=request.data)
    try:
        serializer.user = getattr(request, 'user', None)
        serializer.is_valid(raise_exception=True)
        serializer.set_password_form.save()
        print('success')
        return JsonResponse({"detail": "New password has been saved."}, status=status.HTTP_200_OK)
    except ValidationError:
        error_msgs = []
        error_code = []
        exception = str(ValidationError(serializer.errors))
        for msg in exception.split(":")[1].split("ErrorDetail"):
            if msg.__contains__("string"):
                error_msgs.append(msg.split(",")[0].split("=")[1].split("'")[1])
        for err in error_msgs:
            if err == 'This password is too short. It must contain at least 8 characters.':
                error_code.append(1)
            elif err == 'This password is too common.':
                error_code.append(2)
            elif err == 'This password is entirely numeric.':
                error_code.append(3)
            elif err == 'This field may not be blank.':
                error_code.append(4)
            elif err == 'The two password fields didn’t match.':
                error_code.append(5)
            elif err == 'Invalid password':
                error_code.append(6)
            else:
                error_code.append(7)  # Unknown error, please try again
        return JsonResponse({'Message': error_code}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(operation_summary='send ivitation email', methods=['POST'])
@api_view(['POST'])
# @permission_classes([IsAuthenticated, ])
def send_invite(request):
    # if request.method == 'POST':
        email = request.data.get('email')
        email_validator = EmailValidator()

        try:
            email_validator(email)

            # if check_email_registered(email):
            #     return Response({'message': 'Invalid email address. Please enter a valid email address.'}, status=400)


            smtp_server = 'smtp.qq.com'
            smtp_port = 587  # 通常为587或465
            smtp_username = '1194726682'
            smtp_password = 'tpimvahkhbwwjbab'
            sender_email = '1194726682@qq.com'
            recipient_email = email

            # 创建邮件内容
            # '<a href="https://yourwebsite.com/accept-invitation?token={}">Accept Invitation</a>\n\n'\


            try:
                user = User.objects.get(email=email)
                token = Token.objects.get(user=user)
            except User.DoesNotExist:
                token = None
            except Token.DoesNotExist:
                token = None
            # user = User.objects.get(email=email)
            # token = Token.objects.get(user=user)

            sender = User.objects.get(username=request.data.get('username'))
            survey = Survey.objects.get(id=request.data.get('surveyid'))

            if token is not None:
                email_id = add_email_info(sender, user, survey)
            else:
                email_id = add_email_info(sender, None, survey)


            subject = 'Please confirm this invitation'
            message = 'User {} has invited you to collaborate on a survey - {}\n\n' \
                      'To accept this invitation, please click the following link:\n\n' \
                      '{}accept-invitation?key={}&id={}&email={}\n\n' \
                      'Note: This invitation was intended for {}. If you were not ' \
                      'expecting this invitation, you can ignore this email.\n'.format(request.data.get('username'),
                                                                                       request.data.get('surveyname'),
                                                                                       request.data.get('websiteUrl'),
                                                                                       token,
                                                                                       request.data.get('surveyid'),
                                                                                       email_id,
                                                                                       email, )
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

                return Response({'message': 'Invitation sent successfully'})
            except Exception as e:
                return Response({'message': f'Email could not be sent. Error: {str(e)}'})

        except ValidationError as e:
            # 电子邮件地址无效
            return Response({'message': 'Invalid email address. Please enter a valid email address.'}, status=400)


def check_email_registered(request):
    email = request.GET.get('email')

    if request.method == 'GET':
        try:
            user = User.objects.get(email=email)
            token = Token.objects.get(user=user)
            return JsonResponse({'token': token.key})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token does not exist'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=405)


def get_user_name(request):
    key = request.GET.get('key')


def accept_invitation(request):
    return render(request, 'acceptInvitation.vue')

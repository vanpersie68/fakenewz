from django.conf.urls import url
from django.urls import path, include
from rest_auth.views import PasswordResetConfirmView, PasswordResetView

from account.views import *

urlpatterns = [
    url(r'^password/change/$', reset_password),
    url(r'^password/reset/confirm/$', forget_password),
    url(r'^register/', include('rest_auth.registration.urls')),
    url(r'^update/$', update_user),
    url(r'^', include('rest_auth.urls')),
    path('password/reset/', PasswordResetView.as_view(), name='reset_password'),
    url(r'^verification/email/$', send_verification_email),
    url(r'^delete/$', delete_user),
    url(r'^allauth/', include('allauth.urls')),
    url(r'^send-invite/', send_invite, name='send-invite'),
    url(r'^accept-invitation/$', accept_invitation, name='accept-invitation'),
    url(r'^get_token/$', check_email_registered, name='check-email-registered'),
]



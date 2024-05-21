from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^add_email_info/', views.add_email_info, name='add_email_info'),
    url(r'^check_expiration/<str:sender>/<str:recipient>/<int:questionnaire_id>/', views.check_expiration, name='check_expiration'),
    url(r'^update_verification/(?P<email_info_id>[0-9]+)$', views.update_verification, name='update_verification'),
    url(r'^update_rejected/(?P<email_info_id>[0-9]+)$', views.update_rejected, name='update_rejected'),
    url(r'^get_rejected/(?P<email_info_id>[0-9]+)$', views.getRejected, name='get_rejected'),
    url(r'^get_accept/(?P<email_info_id>[0-9]+)$', views.getAccept, name='get_accept'),
    url(r'^update_accept/(?P<email_info_id>[0-9]+)$', views.update_accept, name='update_accept'),
    url(r'^get_emails/(?P<receiver_id>[0-9]+)$', views.get_emails, name='get_emails'),
]
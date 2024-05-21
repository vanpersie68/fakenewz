from rest_auth.serializers import PasswordResetSerializer
from django.conf import settings
import rest_framework.request
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site

password_reset_email_path = {
    "en": 'account/email/passport_reset/password_reset_email_en.html',
    "ch": "account/email/passport_reset/password_reset_email_cn.html",
    "jp": "account/email/passport_reset/password_reset_email_jp.html",
}

password_reset_email_subject_path = {
    "en": 'account/email/passport_reset/password_reset_subject_en.txt',
    "ch": "account/email/passport_reset/password_reset_subject_cn.txt",
    "jp": "account/email/passport_reset/password_reset_subject_jp.txt",
}


class CustomPasswordResetSerializer(PasswordResetSerializer):
    def save(self):
        request: rest_framework.request.Request = self.context.get('request')
        # Set some values to trigger the send_email method.

        source_domain = "111.231.14.233:8080"
        if 'HTTP_REFERER' in request.META:
            source_domain = request.META['HTTP_REFERER']

        email_template_name = password_reset_email_path['en']
        subject_template_name = password_reset_email_subject_path['en']
        if 'lang' in request.data:
            email_template_name = password_reset_email_path[request.data['lang']]
            subject_template_name = password_reset_email_subject_path[request.data['lang']]

        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'email_template_name': email_template_name,
            'subject_template_name': subject_template_name,
            'extra_email_context': {'source_domain': source_domain},
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)


confirmation_email_path = {
    "en": 'account/email/confirmation/email_confirmation_en',
    "ch": "account/email/confirmation/email_confirmation_cn",
    "jp": "account/email/confirmation/email_confirmation_jp",
}


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)

        source_domain = "111.231.14.233:8080"
        if 'HTTP_ORIGIN' in request.META:
            source_domain = request.META['HTTP_ORIGIN']

        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            'source_domain': source_domain
        }

        lang = 'en'
        if 'accept-language' in request.headers:
            lang = request.headers['accept-language']

        email_template_name = confirmation_email_path[lang]

        self.send_mail(email_template_name, emailconfirmation.email_address.email, ctx)

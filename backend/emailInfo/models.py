from django.db import models
from django.contrib.auth.models import User
from surveybuilder.models import Survey
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db.models import F
from datetime import timedelta

class EmailInfo(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails', null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    expire_time = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.expire_time:
            # 如果 expire_time 未设置，计算其值为 created_at + 7 天
            self.expire_time = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)
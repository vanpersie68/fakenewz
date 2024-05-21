from django.db import models
from django.utils.timezone import now

from surveybuilder.models import Block, Question


class Response(models.Model):
    id = models.BigAutoField(primary_key=True)
    respondent_identifier = models.CharField(null=True, max_length=255)
    uuid = models.CharField(null=True, max_length=255)
    survey = models.IntegerField(null=False)
    create_datetime = models.DateTimeField(default=now)
    end_datetime = models.DateTimeField(default=now)
    contact_info = models.CharField(null=True, max_length=255)
    answer_json = models.CharField(null=True, max_length=5000000)
    user_action = models.CharField(null=True, max_length=5000000)
    user_agent = models.CharField(null=True, max_length=5000000)
    preview = models.BooleanField(default=False)
    completion_rate = models.CharField(null=True, max_length=32)
    camera_state = models.BooleanField(default=True)
    screen_size = models.CharField(null=True, max_length=5000000)
    calibration_acc = models.IntegerField(default=0)
    questionsOrder = models.CharField(null=True, max_length=5000000)


class ResponseBlock(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(null=True, max_length=255)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    gazeData = models.CharField(null=True, max_length=5000000)
    clickEvent = models.CharField(null=True, max_length=5000000)
    create_datetime = models.DateTimeField(null=True, default=now)
    end_datetime = models.DateTimeField(null=True, default=now)


class ResponseQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    block = models.ForeignKey(ResponseBlock, on_delete=models.CASCADE)


class ResponseQuestionAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(null=True, max_length=255)
    question = models.ForeignKey(ResponseQuestion, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000, blank=True, default='')
    answerText = models.CharField(max_length=50000, blank=True, default='')
    answerDecimal = models.DecimalField(default=0, decimal_places=2, max_digits=8)

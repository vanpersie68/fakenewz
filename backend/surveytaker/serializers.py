from rest_framework import serializers
from surveytaker.models import Response, ResponseBlock, ResponseQuestion, ResponseQuestionAnswer


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ['id', 'survey', 'create_datetime', 'end_datetime', 'contact_info', 'answer_json', 'user_agent',
                  'preview', 'completion_rate', 'camera_state', 'calibration_acc', 'screen_size', 'questionsOrder']


class ResponseBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseBlock
        fields = ['id', 'block_id', 'response_id', 'gazeData', 'clickEvent', 'create_datetime', 'end_datetime']


class ResponseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseQuestion
        fields = ['id', 'question', 'block']


class ResponseQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseQuestionAnswer
        fields = ['id', 'question', 'title', 'answerText', 'answerDecimal']

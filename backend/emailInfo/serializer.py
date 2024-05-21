from rest_framework import serializers
from emailInfo.models import EmailInfo

class EmailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailInfo
        fields = ('id', 'sender', 'receiver', 'survey', 'accepted', 'rejected', 'expire_time')
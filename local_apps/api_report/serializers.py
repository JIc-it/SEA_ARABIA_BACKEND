from rest_framework import serializers
from .models import ActionLog
from local_apps.account.models import User


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account_id', 'email', 'mobile', 'role']


class ActionLogSerializer(serializers.ModelSerializer):
    user = UserLogSerializer(required=False, allow_null=True)

    class Meta:
        model = ActionLog
        fields = '__all__'

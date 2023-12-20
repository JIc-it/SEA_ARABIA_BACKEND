from rest_framework import serializers
from .models import ActionLog
from local_apps.account.models import User


class UserLogSerializer(serializers.ModelSerializer):

    state = serializers.CharField(source='state.state', read_only=True, allow_null=True)
    district = serializers.CharField(source='district.district', read_only=True, allow_null=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'mobile', 'state', 'district', 'role']


class ActionLogSerializer(serializers.ModelSerializer):
    user = UserLogSerializer(required=False, allow_null=True)

    class Meta:
        model = ActionLog
        fields = '__all__'

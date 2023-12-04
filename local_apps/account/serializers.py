from rest_framework import serializers
from .models import *

# user cms serializers


class VendorSerializer(serializers.ModelSerializer):
    """vendor listing serializer"""

    location = serializers.CharField(source="profileextra.location")
    status = serializers.CharField(source="company_company_user.status")
    company_id = serializers.CharField(source="company_company_user.id")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "created_at",
            "location",
            "status",
            "company_id",
        ]


class VendorAddSerializer(serializers.ModelSerializer):
    """serializer for adding the vendor"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
        ]


class UserIdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentificationType
        fields = "__all__"


class UserIdentificationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIdentificationData
        fields = "__all__"


# Serializers for viewing in app
class ProfileExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileExtra
        fields = ["id", "location", "image", "dob", "gender"]


class UserSerializerApp(serializers.ModelSerializer):

    """serializer for showing the profile details of the user"""

    profileextra = ProfileExtraSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "profileextra",
        ]


class UserSerializer(serializers.ModelSerializer):
    """user create serialzier"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetSerializerTwo(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)


class OTPVerificationSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()  # User ID associated with the OTP
    otp = serializers.CharField(max_length=6)  # OTP entered by the user

    def validate(self, data):
        # Custom validation logic can be added here, if needed
        return data
    
    
class ForgotPasswordResetSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    new_password = serializers.CharField(required=True)
  
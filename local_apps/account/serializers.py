from rest_framework import serializers
from .models import *
from local_apps.company.serializers import CompanyAddSerializer
from rest_framework.response import Response
from local_apps.company.models import Company
from rest_framework import status

# user cms serializers


class VendorSerializer(serializers.ModelSerializer):
    """vendor listing serializer"""

    location = serializers.CharField(source="profileextra.location")
    status = serializers.CharField(source="company_company_user.status")
    company_id = serializers.CharField(source="company_company_user.id")
    created_by = serializers.CharField(
        source="company_company_user.created_by.first_name"
    )

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
            "created_by",
        ]


class VendorDetailsSerializer(serializers.ModelSerializer):
    """serializer for showing the vendor details"""

    location = serializers.CharField(source="profileextra.location")
    id_number = serializers.CharField(source="useridentificationdata.id_number")
    company_id = serializers.CharField(source="company_company_user.id")
    company_name = serializers.CharField(source="company_company_user.name")
    registration_number = serializers.CharField(
        source="company_company_user.registration_number"
    )
    company_address = serializers.CharField(source="company_company_user.address")
    company_website = serializers.CharField(source="company_company_user.website")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "location",
            "id_number",
            "company_id",
            "company_name",
            "registration_number",
            "company_address",
            "company_website",
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
        fields = ["id_type", "id_number"]


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


class VendorAddDetails(serializers.ModelSerializer):
    """serializer for adding and updating"""

    useridentificationdata = UserIdentificationDataSerializer()
    company_company_user = CompanyAddSerializer()
    location = serializers.CharField(source="profileextra.location")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "useridentificationdata",
            "company_company_user",
            "location",
        ]

    def update(self, instance, validated_data):
        location_data = validated_data.pop("profileextra", {}).get("location", "")
        company_data = validated_data.pop("company_company_user", {})
        user_identification_data = validated_data.pop("useridentificationdata", {})

        profile_instance, _ = ProfileExtra.objects.get_or_create(user=instance)

        if location_data:
            profile_instance.location = location_data
            profile_instance.save()

        company_instance, _ = Company.objects.get_or_create(user=instance)
        company_serializer = CompanyAddSerializer(
            instance=company_instance, data=company_data
        )
        if company_serializer.is_valid():
            company_serializer.save()

        (
            user_identification_instance,
            _,
        ) = UserIdentificationData.objects.get_or_create(user=instance)

        user_identification_serializer = UserIdentificationDataSerializer(
            instance=user_identification_instance, data=user_identification_data
        )
        if user_identification_serializer.is_valid():
            user_identification_serializer.save()

        instance = super().update(instance, validated_data)

        return instance

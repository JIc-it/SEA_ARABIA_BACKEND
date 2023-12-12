from rest_framework import serializers
from .models import *
from local_apps.company.serializers import CompanyAddSerializer
from rest_framework.response import Response
from local_apps.company.models import Company
from rest_framework import status
from local_apps.service.serializers import ServiceSerializer

# user cms serializers


class VendorSerializer(serializers.ModelSerializer):
    """vendor listing serializer"""

    location = serializers.CharField(source="profileextra.location",default=None)
    status = serializers.CharField(source="company_company_user.status",default=None)
    company_id = serializers.CharField(source="company_company_user.id",default=None)
    created_by = serializers.CharField(
        source="company_company_user.created_by.first_name",default=None
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
        fields = ["name", "id"]


class UserIdentificationDataSerializer(serializers.ModelSerializer):
    id_type = UserIdentificationTypeSerializer(read_only =True)

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


class UserListSerializer(serializers.ModelSerializer):
    """ Serializer for listing the user(customer,vendor, and other role types)"""
    location  = serializers.CharField(source = "profileextra.location")
    created_at = serializers.DateTimeField(format="%d-%m-%Y")     
    total_booking = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "mobile",
            "location",
            "created_at",
            "is_active",
            "total_booking",
            "role",
        ]

    def get_total_booking(self,instance):
        return 0
    
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


class VendorAddDetailsSerialzier(serializers.ModelSerializer):
    """Serializer for adding and updating"""

    useridentificationdata = UserIdentificationDataSerializer(read_only=True)
    company_company_user = CompanyAddSerializer(read_only=True)
    location = serializers.CharField(source="profileextra.location", read_only=True)

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

class AllUserDetailsSerializer(serializers.ModelSerializer):
    """ serializer for viewing the details of all the user """

    useridentificationdata = UserIdentificationDataSerializer(read_only=True)
    company_company_user = CompanyAddSerializer(read_only=True)
    profileextra = ProfileExtraSerializer(read_only=True)
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
            "profileextra",
        ]
#----------------------------------------------------------------------mobileapp-------------------------------------------------------------------------
#usersignup 
class UserSignUpSerializer(serializers.ModelSerializer):
    profile_extra = ProfileExtraSerializer(required=False)
    location = serializers.CharField(source="profile_extra.location", required=False)
    images = serializers.ImageField(source="profile_extra.image", required=False)
    dob = serializers.CharField(source="profile_extra.dob", required=False)
    gender = serializers.CharField(source="profile_extra.gender", required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile', 'password','role', 'profile_extra', 'location', 'images', 'dob', 'gender')
        extra_kwargs = {'password': {'write_only': True},}

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_extra_data = validated_data.pop('profile_extra', {})
        validated_data['role'] = 'User'

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create associated ProfileExtra instance
        profile_extra = ProfileExtra.objects.create(user=user, **profile_extra_data)

        # Add related data to the response
        response_data = self.data
        response_data['profile_extra'] = ProfileExtraSerializer(profile_extra).data

        return user, response_data
    

# bookmark

class BookMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = "__all__"

class BookMarkListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Bookmark
        fields = "__all__"





    
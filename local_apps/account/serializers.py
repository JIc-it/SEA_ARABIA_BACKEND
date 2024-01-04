from rest_framework import serializers
from .models import *
from local_apps.company.serializers import CompanyAddSerializer
from rest_framework.response import Response
from local_apps.company.models import Company
from rest_framework import status
from local_apps.service.serializers import ServiceSerializer
from local_apps.booking.models import Booking
from import_export import resources

# user cms serializers


class VendorSerializer(serializers.ModelSerializer):
    """vendor listing serializer"""

    location = serializers.CharField(
        source="profileextra.location", default=None, allow_null=True)
    status = serializers.CharField(
        source="company_company_user.status", default=None, allow_null=True)
    company_id = serializers.CharField(
        source="company_company_user.id", default=None, allow_null=True)
    created_by = serializers.CharField(
        source="company_company_user.created_by.first_name", default=None, allow_null=True
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

    location = serializers.CharField(
        source="profileextra.location", allow_null=True)
    id_number = serializers.CharField(
        source="useridentificationdata.id_number")
    company_id = serializers.CharField(source="company_company_user.id")
    company_name = serializers.CharField(source="company_company_user.name")
    registration_number = serializers.CharField(
        source="company_company_user.registration_number"
    )
    company_address = serializers.CharField(
        source="company_company_user.address")
    company_website = serializers.CharField(
        source="company_company_user.website")
    status = serializers.CharField(
        source="company_company_user.status", default=None)

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
            "status",
            "account_id",
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
    id_type = UserIdentificationTypeSerializer(read_only=True)

    class Meta:
        model = UserIdentificationData
        fields = ["id_type", "id_number"]


class VendorAddDetailsSerialzier(serializers.ModelSerializer):
    """Serializer for adding and updating"""

    useridentificationdata = UserIdentificationDataSerializer(read_only=True)
    company_company_user = CompanyAddSerializer(read_only=True)
    location = serializers.CharField(
        source="profileextra.location", read_only=True)

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


# Serializers for viewing in app


class ProfileExtraSerializer(serializers.ModelSerializer):

    location = serializers.CharField(
        source="location.location", allow_null=True)

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

    # def create(self, validated_data):
    #     password = validated_data.pop("password", None)
    #     instance = self.Meta.model(**validated_data)

    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """ User create Serializer for admin cms """

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
            "password",
            "profileextra"
        ]
        extra_kwargs = {"password": {"write_only": True}}


class UserListSerializer(serializers.ModelSerializer):
    """ Serializer for listing the user(customer,vendor, and other role types)"""

    location = serializers.CharField(source="profileextra.location")
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    total_booking = serializers.SerializerMethodField()
    company_id = serializers.CharField(
        source='company_company_user.id', allow_null=True)
    company_status = serializers.BooleanField(
        source='company_company_user.is_active', allow_null=True)

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
            "company_id",
            "company_status"
        ]

    def get_total_booking(self, instance):
        try:
            if instance.role == "Vendor":
                booking_count = Booking.objects.filter(
                    service__company__user=instance).count()
                return booking_count
            elif instance.role == "User":
                booking_count = Booking.objects.filter(user=instance).count()
                return booking_count
        except Exception as e:
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


class AllUserDetailsSerializer(serializers.ModelSerializer):
    """ serializer for viewing the details of all the user """

    useridentificationdata = UserIdentificationDataSerializer(read_only=True)
    company_company_user = CompanyAddSerializer(read_only=True)
    profileextra = ProfileExtraSerializer(read_only=True)
    company_status = serializers.BooleanField(
        source="company_company_user.is_active", default=None, allow_null=True)
    company_onboard_status = serializers.CharField(
        source="company_company_user.status", default=None, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "account_id",
            "email",
            "mobile",
            "role",
            "first_name",
            "last_name",
            "useridentificationdata",
            "company_company_user",
            "profileextra",
            "company_status",
            "company_onboard_status",
            "is_active"
        ]
# ----------------------------------------------------------------------mobileapp-------------------------------------------------------------------------
# usersignup


class UserSignUpSerializer(serializers.ModelSerializer):
    profile_extra = ProfileExtraSerializer(required=False)
    location = serializers.CharField(
        source="profile_extra.location", required=False)
    images = serializers.ImageField(
        source="profile_extra.image", required=False)
    dob = serializers.CharField(source="profile_extra.dob", required=False)
    gender = serializers.CharField(
        source="profile_extra.gender", required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'mobile', 'password', 'role',
                  'profile_extra', 'location', 'images', 'dob', 'gender')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        password = validated_data.pop('password')
        profile_extra_data = validated_data.pop('profile_extra', {})
        validated_data['role'] = 'User'

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # Create associated ProfileExtra instance
        profile_extra = ProfileExtra.objects.create(
            user=user, **profile_extra_data)

        # Add related data to the response
        response_data = self.data
        response_data['profile_extra'] = ProfileExtraSerializer(
            profile_extra).data

        return user, response_data


# bookmark

class BookmarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bookmark
        fields = "__all__"


class BookmarkListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"


class UserUpdatedSerializer(serializers.ModelSerializer):
    profileextra = ProfileExtraSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['email', 'mobile', 'role', 'profileextra']

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.mobile = validated_data.get('mobile', instance.mobile)
    #     instance.role = validated_data.get('role', instance.role)

    #     instance.save()

    #     profile_extra_data = validated_data.pop('profile_extra', {})

    #     profile_extra_instance, created = ProfileExtra.objects.get_or_create(
    #         user=instance,
    #         defaults=profile_extra_data
    #     )

    #     if not created:
    #         for key, value in profile_extra_data.items():
    #             setattr(profile_extra_instance, key, value)
    #         profile_extra_instance.save()
    #     return instance


class GuestSerializer(serializers.ModelSerializer):
    """ serializer for Guest user model """

    class Meta:
        model = Guest
        fields = ["first_name", "last_name", "mobile", "email", "location"]


class VendorListExport(resources.ModelResource):
    created_by = resources.Field(
        column_name='created_by', attribute='company_company_user__created_by__first_name')
    location = resources.Field(
        column_name='location', attribute='profileextra__location')
    status = resources.Field(column_name='status',
                             attribute='company_company_user__status')

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "location",
            "created_at",
            "created_by",
            "status",
        ]

        export_order = fields


class CustomerListExport(resources.ModelResource):
    location = resources.Field(
        column_name='location', attribute='profileextra__location')
    status = resources.Field(column_name='status', attribute='is_active')
    bookings = resources.Field(
        column_name='bookings', attribute='booking_booking_user')

    # def dehydrate_bookings_count(self, user):
    #     return user.booking_booking_user.count()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "location",
            "created_at",
            "bookings",
            "status",
        ]

        export_order = fields

    def booking_booking_user(self, user):
        return user.booking_booking_user

    def export_field(self, field, obj):
        if field.attribute == 'booking_booking_user':
            return self.calculate_booking_count(obj)
        return super(CustomerListExport, self).export_field(field, obj)

    def calculate_booking_count(self, user):
        return Booking.objects.filter(user=user).count()


class GuestsListExport(resources.ModelResource):
    class Meta:
        model = Guest
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "location",
        ]

        export_order = fields


class OnboardVendorsListExport(resources.ModelResource):
    location = resources.Field(
        column_name='location', attribute='profileextra__location')
    status = resources.Field(column_name='status', attribute='is_active')
    bookings = resources.Field(
        column_name='bookings', attribute='booking_booking_user')

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile",
            "location",
            "created_at",
            "bookings",
            "status",
        ]

        export_order = fields

    def booking_booking_user(self, user):
        return user.booking_booking_user

    def export_field(self, field, obj):
        if field.attribute == 'booking_booking_user':
            return self.calculate_booking_count(obj)
        return super(OnboardVendorsListExport, self).export_field(field, obj)

    def calculate_booking_count(self, user):
        return Booking.objects.filter(user=user).count()


class GccLocationSerializer(serializers.ModelSerializer):
    """ Serialize GCC Locations """

    class Meta:
        model = GCCLocations
        fields = [
            "id",
            "location",
            "country_flag"
        ]

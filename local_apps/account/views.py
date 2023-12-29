import re
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
from local_apps.company.filters import CompanyFilter
from .filters import *
from local_apps.company.models import Company, OnboardStatus
from rest_framework.views import APIView
from django.utils import timezone
from .models import PasswordReset
from django.contrib.auth import get_user_model
import random
from local_apps.message_utility.views import mail_handler
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Case, When, IntegerField, Sum
import datetime
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
import requests
from urllib.parse import unquote, quote
import secrets
import string

# Google OAuth 2.0 configuration
GOOGLE_CLIENT_ID = '28175996828-ls8r9c9l27r7kfvj28tv0ijrhgujt296.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
GOOGLE_REDIRECT_URI = 'http://localhost:8888/google_callback'

GOOGLE_AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'
scopes = ['email', 'profile', 'https://www.googleapis.com/auth/user.phonenumbers.read']
scope_quoted = quote(" ".join(scopes))


def generate_random_password(length=12):
    # Define the characters to include in the password
    characters = string.ascii_letters + string.digits + string.punctuation

    # Use secrets.choice to select random characters for the password
    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password


def validate_gmail(email):
    # Define the regular expression for a Gmail email address
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@gmail\.com$')

    # Use the match() method to check if the email matches the pattern
    match = pattern.match(email)

    # Return True if the email is a valid Gmail address, otherwise False
    return bool(match)


class GoogleAuth(APIView):
    def get(self, request):
        try:
            authorization_url = (
                f'{GOOGLE_AUTHORIZATION_URL}?client_id={GOOGLE_CLIENT_ID}'
                f'&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope={scope_quoted}'
            )
            return Response(authorization_url, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            code = request.data.get('code', None)
            if code:
                auth_code = unquote(code)
                token_data = {
                    'code': auth_code,
                    'client_id': GOOGLE_CLIENT_ID,
                    'client_secret': GOOGLE_CLIENT_SECRET,
                    'redirect_uri': GOOGLE_REDIRECT_URI,
                    'grant_type': 'authorization_code'
                }
                token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
                token_info = token_response.json()
                user_info_response = requests.get(
                    GOOGLE_USER_INFO_URL, headers={'Authorization': f'Bearer {token_info["access_token"]}'}
                )
                user_info = user_info_response.json()
                email = user_info['email']
                first_name = user_info['given_name']
                last_name = user_info['family_name']

                if validate_gmail(email):
                    if User.objects.filter(email=email).exists():
                        user = User.objects.get(email=email)
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        refresh_token = str(refresh)
                        return Response({'access': access_token, 'refresh': refresh_token}, status=status.HTTP_200_OK)
                    else:
                        user = User.objects.create_user(first_name=first_name,
                                                        last_name=last_name,
                                                        email=email,
                                                        role='User',
                                                        password=generate_random_password())
                        refresh = RefreshToken.for_user(user)
                        access_token = str(refresh.access_token)
                        refresh_token = str(refresh)
                        return Response({'access': access_token, 'refresh': refresh_token},
                                        status=status.HTTP_201_CREATED)
                else:
                    raise Exception('Invalid gmail address found')
            else:
                raise Exception('Code must be provided')

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# custom Auth


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_id = user.id
            print(user_id)

            return Response({
                'detail': 'Login successful!',
                'access_token': access_token,
                'refresh_token': refresh_token,
                # 'user_id':user_id

            }, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(
                'Invalid email or password. Please try again.')


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

#   User CRUD View


class UserCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    """ list all users """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "profileextra__location",
        "email",
        "mobile"
    ]

    filterset_class = UserFilter


class UserUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


#   Profile extra views
class ProfileExtraCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileExtraSerializer


# cms views


class VendorList(generics.ListAPIView):
    """ view for listing the vendor in cms """

    queryset = User.objects.filter(
        role="Vendor", company_company_user__is_onboard=False)
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "mobile",
        "email",
        "first_name",
        "last_name",
        "profileextra__location",
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "created_at",
        "profileextra__location",
    ]
    filterset_class = VendorFilter


class VendorDetailsList(generics.RetrieveAPIView):
    queryset = User.objects.filter(role="Vendor")
    serializer_class = VendorDetailsSerializer


class VendorAdd(generics.CreateAPIView):
    """view for creating new vendor"""

    serializer_class = VendorAddSerializer

    def perform_create(self, serializer):
        location_data = self.request.data.get("location")
        created_by = self.request.user
        user = serializer.save()
        if location_data:
            profile_extra = ProfileExtra.objects.create(
                user=user, location=location_data
            )
        new_lead = OnboardStatus.objects.get(order=1)
        Company.objects.create(
            user=user, created_by=created_by, status=new_lead)


class VendorDetailsAdd(generics.UpdateAPIView):
    serializer_class = VendorAddDetailsSerialzier
    queryset = User.objects.filter(role="Vendor")

    def update(self, request, *args, **kwargs):
        try:

            # taking the data
            location_data = request.data.get("location", {})
            company_data = request.data.get("company_company_user", {})
            user_identification_data = request.data.get(
                "useridentificationdata", {})
            service_category = company_data.get('service_summary', [])

            user_id_type = user_identification_data.get('id_type', None)
            user_id_number = user_identification_data.get('id_number', None)

            #   get user instance
            user = User.objects.get(id=kwargs["pk"])

            #   user details

            email = request.data.get("email", None)
            mobile = request.data.get("mobile", None)
            first_name = request.data.get("first_name", None)
            last_name = request.data.get("last_name", None)

            if email:
                user.email = email

            if mobile:
                user.mobile = mobile

            if first_name:
                user.first_name = first_name

            if last_name:
                user.last_name = last_name

            user.save()

            #   updating the user profile extra
            profile_instance, created = ProfileExtra.objects.get_or_create(
                user=user)
            if location_data:
                profile_instance.location = location_data
                profile_instance.save()

            #   updating the company details VendorAddDetailsSerialzier

            company_instance, _ = Company.objects.get_or_create(user=user)
            company_serializer = CompanyAddSerializer(
                instance=company_instance, data=company_data)
            if company_serializer.is_valid():
                company_serializer.save()

                if service_category:
                    company_instance.service_summary.set(service_category)

            #   updating the user identification data
            useridentification_instance, _, = UserIdentificationData.objects.get_or_create(
                user=user)

            if user_id_type and user_id_number:
                idType = get_object_or_404(
                    UserIdentificationType, id=user_id_type)
                useridentification_instance.id_type = idType
                useridentification_instance.id_number = user_id_number
                useridentification_instance.save()

            serializer = VendorAddDetailsSerialzier(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


# ? Lead management card APIs

class VendorLeadCount(APIView):
    """ vendor related counts """

    def get(self, request):
        try:

            total_lead_count = User.objects.filter(
                role="Vendor", company_company_user__is_onboard=False).count()
            total_active_vendors = Company.objects.filter(
                is_onboard=True).count()
            seven_days = datetime.date.today() - datetime.timedelta(7)
            # ? takes the count of the leads that are generated in the last 7 days
            new_leads = User.objects.filter(
                created_at__date__gte=seven_days, role="Vendor").count()
            active_vendors = Company.objects.filter(is_onboard=True).annotate(
                service_count=Count(
                    "service", filter=Q(service__is_active=True))
            ).filter(service_count__gt=0)
            total_count = {
                "total_lead": total_lead_count,
                "onboarded_vendors": total_active_vendors,
                "new_leads": new_leads,
                "active_vedors": active_vendors.count()
            }
            return Response(total_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


# ? user count cards

class UserCountList(APIView):
    """ count of the users """

    def get(self, request):
        try:
            user_count = User.objects.filter(role="User").count()
            return Response({"user_count": user_count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class VendorCountList(APIView):
    """ vendor coutn cards """

    def get(self, request):
        try:
            total_vendor = User.objects.all().aggregate(
                total_count=Count("pk"),
                active_vendor=Sum(
                    Case(When(is_active=True, then=1), default=0, output_field=IntegerField())),
                inactive_vendor=Sum(
                    Case(When(is_active=False, then=1), default=0, output_field=IntegerField())),
            )

            return Response(total_vendor, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class AllUserDetails(generics.RetrieveAPIView):
    """ List all the user(different roles) details """

    queryset = User.objects.all()
    serializer_class = AllUserDetailsSerializer


class UserIdTypeList(generics.ListAPIView):
    """ list the id types """

    serializer_class = UserIdentificationTypeSerializer
    queryset = UserIdentificationType.objects.all()


# -----------------------------------------------------------Authenitaction-Section/OTP/FORGOTPASSWORD-----------------------------------------------------------------------------------------------------------------------------#


def generate_otp():
    print("generate_otp")
    return "".join(random.choice("0123456789") for _ in range(6))


class RequestOTPView(APIView):
    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"]
                try:
                    print(email)
                    user = User.objects.get(email=email)
                    print(user)
                except User.DoesNotExist:
                    return Response(
                        {"detail": "User with this email does not exist."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                otp = generate_otp()
                expires_at = timezone.now() + timezone.timedelta(minutes=5)
                password_reset, created = PasswordReset.objects.get_or_create(
                    user=user, defaults={"otp": otp, "expires_at": expires_at}
                )
                if not created:
                    password_reset.otp = otp
                    password_reset.expires_at = expires_at
                    password_reset.save()
                data = {
                    "name": str(user.first_name) if user.first_name else "DMS User",
                    "otp": str(otp),
                }
                subject = "Sea Arabia Account Password Reset"
                email_template = "message_utility/password_otp.html"
                mail_handler(
                    mail_type="single",
                    to=[email],
                    subject=subject,
                    data=data,
                    template=email_template,
                )
                return Response(
                    {"detail": "OTP sent successfully.",
                     "user_id": str(user.id)},
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        try:
            serializer = OTPVerificationSerializer(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data["user_id"]
                otp = serializer.validated_data["otp"]
                password_reset = PasswordReset.objects.filter(
                    user_id=user_id, otp=otp
                ).first()
                if not password_reset:
                    return Response(
                        {"detail": "Invalid OTP or OTP has expired."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                if password_reset.expires_at < timezone.now():
                    return Response(
                        {"detail": "OTP has expired."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(
                    {"detail": "OTP verified successfully."}, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ForgotResetPasswordViewsnew(APIView):
    def post(self, request):
        try:
            serializer = ForgotPasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                user_id = serializer.validated_data["user_id"]
                new_password = serializer.validated_data["new_password"]
                password_reset = PasswordReset.objects.get(user_id=user_id)
                user = password_reset.user
                user.set_password(new_password)
                user.save()
                password_reset.delete()  # Optionally, you can delete the PasswordReset object
                return Response(
                    {"detail": "Password reset successful."}, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class CheckFirstTimeLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_first_time:
            return Response(
                {
                    "is_first_time": True,
                    "message": "First-time login. Please reset your password.",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"is_first_time": False, "message": "Not a first-time login."},
                status=status.HTTP_200_OK,
            )


User = get_user_model()


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if new_password and confirm_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.is_first_time = False
                user.save()
                return Response(
                    {"message": "Password reset successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "New password and confirm password do not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Empty passwords "}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["confirm_password"]

        if current_password and new_password and confirm_password:
            if not user.check_password(current_password):
                return Response(
                    {"error": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password has been reset successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "New password and confirm password do not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"error": "Please provide all fields"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


def emilres(request):
    return render(request, "email.html")


# ------------------------------------------------------------------------mobilepp-----------------------------------------------------------------#


class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {'message': 'User registered successfully'}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BookMarkCreationAPI(generics.CreateAPIView):
    """bookmark creation"""
    queryset = Bookmark.objects.all()
    serializer_class = BookMarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class BookMarkListView(generics.ListAPIView):
#     """bookmark listing"""
#     serializer_class = BookMarkListSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):

#         return Bookmark.objects.filter(user=self.request.user)

class BookMarkListView(generics.ListAPIView):
    """bookmark listing"""
    serializer_class = BookMarkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class BookMarkDeleteView(generics.DestroyAPIView):
    """bookmark deletion"""
    queryset = Bookmark.objects.all()
    serializer_class = BookMarkListSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'message': 'Bookmark deleted successfully'}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializerApp
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            profile_extra = ProfileExtra.objects.get(user=user)
        except ProfileExtra.DoesNotExist:
            profile_extra = None

        user.profile_extra = profile_extra
        return user


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdatedSerializer
    permission_classes = [IsAuthenticated]

    # def get_object(self):
    #     return self.request.user
    # FIXME::    get object code commented so that user can be taken from the user id passed

    def update(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk', None)
            email = request.data.get('email', None)
            mobile = request.data.get('mobile', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            profile_extra = request.data.get('profileextra', {})
            location = profile_extra.get('location', None)
            dob = profile_extra.get('dob', None)
            gender = profile_extra.get('gender', None)
            user_instance = get_object_or_404(User, id=user_id)
            profile_instance, _ = ProfileExtra.objects.get_or_create(
                ProfileExtra, user=user_instance)

            if email:
                user_instance.email = email
            if mobile:
                user_instance.mobile = mobile
            if first_name:
                user_instance.first_name = first_name
            if last_name:
                user_instance.last_name = last_name

            if location:
                profile_instance.location = location

            if dob:
                profile_instance.dob = dob

            if gender:
                profile_instance.gender = gender.title()

            user_instance.save()
            profile_instance.save()
            serializer = UserUpdatedSerializer(user_instance)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class GuestUserList(generics.ListAPIView):
    serializer_class = GuestSerializer
    queryset = Guest.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "email",
        "mobile",
        "location"
    ]


# Export as CSV

class ExportVendorCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(
            role="Vendor")
        resource = VendorListExport()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendor_list.csv"'

        return response


class ExportCustomerCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(
            role="User")
        resource = CustomerListExport()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'

        return response


class ExportGuestsCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Guest.objects.all()
        resource = GuestsListExport()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="guests_list.csv"'

        return response


class ExportOnboardVendorsCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(
            role="Vendor", company_company_user__is_onboard=True)
        resource = OnboardVendorsListExport()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendor_users_list.csv"'

        return response

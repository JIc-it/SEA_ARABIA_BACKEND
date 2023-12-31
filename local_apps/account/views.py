import re
import random
import secrets
import string
import requests
import datetime
from urllib.parse import unquote, quote
from utils.action_logs import create_log
from datetime import datetime as dt
from django.core.serializers import serialize
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Case, When, IntegerField, Sum
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from local_apps.company.filters import CompanyFilter
from local_apps.company.models import Company, OnboardStatus
from local_apps.message_utility.views import mail_handler
from .filters import *
from .models import *
from .serializers import *

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
                f'{settings.GOOGLE_AUTHORIZATION_URL}?client_id={settings.GOOGLE_CLIENT_ID}'
                f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}&response_type=code&scope={scope_quoted}'
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
                    'client_id': settings.GOOGLE_CLIENT_ID,
                    'client_secret': settings.GOOGLE_CLIENT_SECRET,
                    'redirect_uri': settings.GOOGLE_REDIRECT_URI,
                    'grant_type': 'authorization_code'
                }
                token_response = requests.post(
                    settings.GOOGLE_TOKEN_URL, data=token_data)
                token_info = token_response.json()
                user_info_response = requests.get(
                    settings.GOOGLE_USER_INFO_URL, headers={
                        'Authorization': f'Bearer {token_info["access_token"]}'}
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
        try:
            email = request.data.get('email')
            password = request.data.get('password')

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                user_id = user.id

                return Response({
                    'detail': 'Login successful!',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    # 'user_id':user_id

                }, status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed(
                    'Invalid email or password. Please try again.')
        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------------------------------------------------------------------------------------------------------

#   User CRUD View


class UserCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data before the user creation
            value_before = serialize('json', [User()])

            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            email = request.data.get("email")
            mobile = request.data.get("mobile")
            location = request.data.get("location")
            gender = request.data.get("gender")
            dob = request.data.get("dob")
            password = request.data.get("password")
            role = request.data.get("role")

            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email,
                                            role=role,
                                            mobile=mobile,
                                            password=password)
            value_after = serialize('json', [user])
            if location:
                location_instance = GCCLocations.objects.get(id=location)

                ProfileExtra.objects.create(
                    user=user, location=location_instance, gender=gender.title(), dob=dob)
            data = UserCreateSerializer(user)

            # Log the user creation action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="User",
                action='Created',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='User',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return Response(data.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)



class UserList(generics.ListAPIView):
    """ list all users """

    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "first_name",
        "last_name",
        "profileextra__location__country",
        "email",
        "mobile"
    ]

    filterset_class = UserFilter


class UserUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Get the user instance before the update
            user_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [user_before_update])

            response = super().update(request, *args, **kwargs)

            # Get the updated user instance
            user_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [user_after_update])

            # Log the user update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="User",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='User',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return response
        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)


#   Profile extra views
class ProfileExtraCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileExtraSerializer


# cms views


class VendorList(generics.ListAPIView):
    """ view for listing the vendor in cms """

    queryset = User.objects.filter(role="Vendor", company_company_user__is_onboard=False)
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = [
        "mobile",
        "email",
        "first_name",
        "last_name",
        "profileextra__location__country",
    ]
    ordering_fields = [
        "first_name",
        "last_name",
        "created_at",
        "profileextra__location__country",
    ]
    filterset_class = VendorFilter


class VendorDetailsList(generics.RetrieveAPIView):
    queryset = User.objects.filter(role="Vendor")
    serializer_class = VendorDetailsSerializer


# class VendorAdd(generics.CreateAPIView):
#     """view for creating new vendor"""
#
#     serializer_class = VendorAddSerializer
#
#     def perform_create(self, serializer):
#         location_data = self.request.data.get("location")
#         created_by = self.request.user
#         user = serializer.save()
#
#         if location_data:
#             location_instance = GCCLocations.objects.get(id=location_data)
#             profile_extra = ProfileExtra.objects.create(
#                 user=user, location=location_instance
#             )
#         new_lead = OnboardStatus.objects.get(order=1)
#         Company.objects.create(
#             user=user, created_by=created_by, status=new_lead)

class VendorAdd(generics.CreateAPIView):
    """View for creating a new vendor"""

    serializer_class = VendorAddSerializer

    def perform_create(self, serializer):
        try:
            # Serialize the data before the vendor creation
            value_before = serialize('json', [Company()])

            location_data = self.request.data.get("location")
            created_by = self.request.user
            user = serializer.save()

            if location_data:
                location_instance = GCCLocations.objects.get(id=location_data)
                ProfileExtra.objects.create(
                    user=user, location=location_instance
                )

            new_lead = OnboardStatus.objects.get(order=0)
            company = Company.objects.create(
                user=user, created_by=created_by, status=new_lead)

            # Serialize the data after the vendor creation
            value_after = serialize('json', [company])

            # Log the vendor creation action
            log_user = self.request.user if self.request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Company",
                action='Created',
                user=log_user
            )

            create_log(
                user=self.request.user,
                model_name='Company',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )
        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)


class VendorDetailsAdd(generics.UpdateAPIView):
    serializer_class = VendorAddDetailsSerialzier
    queryset = User.objects.filter(role="Vendor")

    def update(self, request, *args, **kwargs):
        try:

            # Get the user instance before the update
            user_before_update = self.get_object()

            # Serialize the data before the update
            value_before = serialize('json', [user_before_update])

            # taking the data
            location_data = request.data.get("location", {})
            company_data = request.data.get("company_company_user", {})
            user_identification_data = request.data.get("useridentificationdata", {})
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
                location_instance = GCCLocations.objects.get(id=location_data)
                profile_instance.location = location_instance
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

            # Get the updated user instance
            user_after_update = self.get_object()

            # Serialize the data after the update
            value_after = serialize('json', [user_after_update])

            # Log the user update action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="User",
                action='Updated',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='User',
                action_value='Update',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

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
            # ? takes the count of the leads that are generated in the last 7 days
            seven_days = dt.today() - datetime.timedelta(7)
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


# @method_decorator(cache_page(60 * 15), name='dispatch')
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


# @method_decorator(cache_page(60 * 15), name='dispatch')
class AllUserDetails(generics.RetrieveAPIView):
    """ List all the user(different roles) details """

    queryset = User.objects.all()
    serializer_class = AllUserDetailsSerializer


class UserIdTypeList(generics.ListAPIView):
    """ list the id types """

    serializer_class = UserIdentificationTypeSerializer
    queryset = UserIdentificationType.objects.all()


# -----------------------Authenitaction-Section/OTP/FORGOTPASSWORD--------------------------------------#


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
                    user = User.objects.get(email=email)
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


# ALL USER RESET PASSWORD FOR ADMIN CMS
class AllUserResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data.get("user_id")
            new_password = request.data.get("new_password")
            confirm_password = request.data.get("confirm_password")

            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND, )

            if new_password and confirm_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.save()
                    return Response(
                        {"message": "Password reset successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"error": "New password and confirm password do not match."},
                        status=status.HTTP_400_BAD_REQUEST, )
            else:
                return Response({"error": "Empty passwords "}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def emilres(request):
    return render(request, "email.html")


# ---------------------------mobilepp-----------------------------------#


# class UserSignUp(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSignUpSerializer
#
#     def post(self, request, *args, **kwargs):
#         serializer = UserSignUpSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response_data = {'message': 'User registered successfully'}
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserSignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        try:
            email = request.data.get('email', None)
            mobile = request.data.get('mobile', None)
            # profile_extra = request.data.get('profileextra', {})
            location = request.data.get('location', None)
            dob = request.data.get('dob', None)
            gender = request.data.get('gender', None)

            # Create a new user instance
            user_instance = User.objects.create(
                email=email,
                mobile=mobile
            )

            # Create a new profile instance and associate it with the user
            ProfileExtra.objects.create(
                user=user_instance,
                location=GCCLocations.objects.get(
                    id=location) if location else None,
                dob=dob,
                gender=gender.title() if gender else None
            )

            serializer = UserUpdatedSerializer(user_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class BookmarkCreateAPIView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def perform_create(self, serializer):
        # Set the user field to the logged-in user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check if the user has already bookmarked this service
        user = self.request.user
        service = serializer.validated_data['service']
        if Bookmark.objects.filter(user=user, service=service).exists():
            return Response({"message": "You have already bookmarked this service."},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BookMarkListView(generics.ListAPIView):
    """bookmark listing"""
    serializer_class = BookmarkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)


class BookMarkDeleteView(generics.DestroyAPIView):
    """Bookmark deletion"""
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkListSerializer
    lookup_url_kwarg = 'service_id'
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            service = Service.objects.get(id=self.kwargs['service_id'])
            if service and Bookmark.objects.filter(user=request.user, service=service).exists():
                Bookmark.objects.get(
                    user=request.user, service=service).delete()
                return Response(data={'message': 'Bookmark deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': 'Bookmark delete failed'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializerApp
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            user = self.request.user
            try:
                profile_extra = ProfileExtra.objects.get(user=user)
            except ProfileExtra.DoesNotExist:
                profile_extra = None

            user.profile_extra = profile_extra
            return user
        except Exception as e:
            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdatedSerializer
    permission_classes = [IsAuthenticated]


    def update(self, request, *args, **kwargs):
        try:
            user_id = kwargs.get('pk', None)
            email = request.data.get('email', None)
            mobile = request.data.get('mobile', None)
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            profile_extra_data = request.data.get('profileextra', {})
            location_id = profile_extra_data.get('location', None)
            dob = profile_extra_data.get('dob', None)
            gender = profile_extra_data.get('gender', None)
            image = request.data.get('image', None)  # Get the image from request data

            user_instance = get_object_or_404(User, id=user_id)
            profile_instance, _ = ProfileExtra.objects.get_or_create(user=user_instance)

            if email:
                user_instance.email = email
            if mobile:
                user_instance.mobile = mobile
            if first_name:
                user_instance.first_name = first_name
            if last_name:
                user_instance.last_name = last_name
            if location_id:
                location_instance = GCCLocations.objects.get(id=location_id)
                profile_instance.location = location_instance
            if dob:
                dob_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
                profile_instance.dob = dob_date
            if gender:
                profile_instance.gender = gender.title()
            if image:
                profile_instance.image = image

            user_instance.save()
            profile_instance.save()
            serializer = UserUpdatedSerializer(user_instance)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

class GuestUserList(generics.ListAPIView):
    ''' guest user listing for cms '''
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
        try:
            queryset = User.objects.filter(role="Vendor")
            resource = VendorListExport()
            dataset = resource.export(queryset)
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="vendor_list.csv"'
            return response
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ExportCustomerCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = User.objects.filter(role="User")
            resource = CustomerListExport()
            dataset = resource.export(queryset)
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="customer_list.csv"'
            return response
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ExportGuestsCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = Guest.objects.all()
            resource = GuestsListExport()
            dataset = resource.export(queryset)
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="guests_list.csv"'
            return response
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ExportOnboardVendorsCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            queryset = User.objects.filter(role="Vendor", company_company_user__is_onboard=True)
            resource = OnboardVendorsListExport()
            dataset = resource.export(queryset)
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="vendor_users_list.csv"'
            return response
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class GCCLocationsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            locations = GCCLocations.objects.filter(is_active=True)
            serializer = GCCLocationsSerializer(locations, many=True)
            formatted_locations = [
                {
                    'code': item['country_code'],
                    'label': item['country'],
                    'name': item['country_code'],
                    'id': item['id']
                }
                for item in serializer.data
            ]
            return Response(formatted_locations, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = Notification.objects.all()
        user = self.request.user
        if user.role in ['Admin', 'Staff']:
            query = query.filter(is_admin=True).order_by('-created_at')
        else:
            query = query.filter(user=user).order_by('-created_at')
        return query


class NotificationUpdateView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.read_by.add(request.user)
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

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

from django.contrib.auth import authenticate, login
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

#custom Auth


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
            
            user_id=user.id
            print(user_id)

            return Response({
                'detail': 'Login successful!',
                'access_token': access_token,
                'refresh_token': refresh_token,
                # 'user_id':user_id
                
            }, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed('Invalid email or password. Please try again.')
        




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------        







#   User CRUD View


class UserCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDelete(generics.DestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSerializerView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializerApp


#   Profile extra views
class ProfileExtraCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ProfileExtraSerializer


# cms views


class VendorSerializerList(generics.ListAPIView):

    """view for listing the vendor in cms"""

    queryset = User.objects.filter(role="Vendor")
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
        Company.objects.create(user=user, created_by=created_by, status=new_lead)


class VendorDetailsAdd(generics.UpdateAPIView):
    serializer_class = VendorAddDetailsSerialzier
    queryset = User.objects.filter(role="Vendor")

    def update(self, request, *args, **kwargs):
        try:

            # taking the data 
            location_data = request.data.get("location", {})
            company_data = request.data.get("company_company_user", {})
            user_identification_data = request.data.get("useridentificationdata", {})
            service_category = company_data.get('service_summary',[])

            user_id_type = user_identification_data.get('id_type',None)
            user_id_number = user_identification_data.get('id_number',None)

            #   get user instance
            user = User.objects.get(id=kwargs["pk"])

            #   user details 

            email = request.data.get("email",None)
            mobile = request.data.get("mobile",None)
            first_name = request.data.get("first_name",None)
            last_name = request.data.get("last_name",None)

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
            profile_instance, created = ProfileExtra.objects.get_or_create(user=user)
            if location_data:
                profile_instance.location = location_data
                profile_instance.save()

            #   updating the company details 

            company_instance, _ = Company.objects.get_or_create(user=user)
            company_serializer = CompanyAddSerializer(instance=company_instance, data=company_data)
            if company_serializer.is_valid():
                company_serializer.save()

                if service_category:
                    company_instance.service_summary.set(service_category)
            
            #   updating the user identification data
            useridentification_instance,_,= UserIdentificationData.objects.get_or_create(user=user)
            
            if user_id_type and user_id_number:
                idType = get_object_or_404(UserIdentificationType, id=user_id_type)
                useridentification_instance.id_type = idType
                useridentification_instance.id_number = user_id_number
                useridentification_instance.save()
                
            serializer = VendorAddDetailsSerialzier(user)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"Error: {str(e)}",status= status.HTTP_400_BAD_REQUEST)
        

        

class VendorPersonalList(generics.RetrieveAPIView):
    queryset = User.objects.filter(role="Vendor")
    serializer_class = VendorAddDetailsSerialzier


class UserIdTypeList(generics.ListAPIView):
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
                    {"detail": "OTP sent successfully.", "user_id": str(user.id)},
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
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
       
        serializer.save(user=self.request.user)


class BookMarkListView(generics.ListAPIView):
    """bookmark listing"""
    serializer_class = BookMarkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return BookMark.objects.filter(user=self.request.user)
    

class BookMarkDeleteView(generics.RetrieveDestroyAPIView):
    """book deletion"""
    queryset = BookMark.objects.all()
    serializer_class = BookMarkListSerializer
    lookup_field ='pk'

 
    

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            profile_extra = ProfileExtra.objects.get(user=user)
        except ProfileExtra.DoesNotExist:
            profile_extra = None

        user.profile_extra = profile_extra
        return user
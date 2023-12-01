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
from local_apps.company.models import Company

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


class VendorAdd(generics.CreateAPIView):
    """view for creating new vendor"""

    serializer_class = VendorAddSerializer

    def perform_create(self, serializer):
        location_data = self.request.data.get("location")
        user = serializer.save()
        if location_data:
            profile_extra = ProfileExtra.objects.create(
                user=user, location=location_data
            )
        Company.objects.create(user=user)

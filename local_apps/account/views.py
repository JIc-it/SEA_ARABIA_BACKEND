from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from .serializers import *
from local_apps.company.filters import CompanyFilter
from .filters import *

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


class VendorSerializerList(generics.ListAPIView):
    queryset = User.objects.filter(role="Vendor")
    serializer_class = VendorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "mobile",
        "email",
        "first_name",
        "last_name",
        "profileextra__location",
    ]
    filterset_class = VendorFilter

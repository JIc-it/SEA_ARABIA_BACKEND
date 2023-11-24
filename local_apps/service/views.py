from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from .serializers import *
from .filters import *


class OccassionList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Occasion.objects.all()
    serializer_class = OccassionSerializer


# vendorPrice Type Views


class VendorPriceTypeList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = VendorPriceType.objects.all()
    serializer_class = VendorPriceTypeSerializer


class VendorPriceTypeCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = VendorPriceType.objects.all()
    serializer_class = VendorPriceTypeSerializer


class VendorPriceTypeUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = VendorPriceType.objects.all()
    serializer_class = VendorPriceTypeSerializer


# Destination Type Views


class DestinationList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


# Amenity Type Views


class AmenityList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


# Category Type Views


class CategoryList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# SubCategory Type Views


class SubCategoryList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SubCategoryFilter


# Service Type Views


class ServiceList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ServiceFilter


class ServiceCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceView(generics.RetrieveAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


# # Service Type Views


# class ServiceList(generics.ListAPIView):
#     # permission_classes = [IsAuthenticated]
#     queryset = Service.objects.all()
#     serializer_class = ServiceSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_class = ServiceFilter

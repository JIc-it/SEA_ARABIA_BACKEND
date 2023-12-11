from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import *
from .serializers import *
from .filters import *
from django.shortcuts import get_object_or_404
from local_apps.main.serializers import CategorySerializer, SubCategorySerializer
from datetime import datetime

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
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_class = SubCategoryFilter


# Service Type Views


class ServiceList(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ExploreMoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "name",
        "occasions__name",
        "amenities__name",
        "destination__name",
    ]
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


# Service Price Views


class ServicePriceUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


# Service Image Views


class ServiceImageUpdate(generics.UpdateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceImage.objects.all()
    serializer_class = ServiceImageSerializer


# service review views


class ServiceReviewCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ServiceReviewSerializer


class ServiceReviewUpdate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer


class ServiceFilterList(generics.ListAPIView):
    """View for filtering the service in service review listing section"""

    serializer_class = ServiceFilterListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name"]
    filterset_class = ServiceFilter

    def get_queryset(self):
        user = self.request.user
        service_list = Service.objects.filter(company__user=user)
        return service_list


class ServiceReviewList(generics.ListAPIView):
    """view for showing the reviews realted to the particular service"""

    # permission_classes = [IsAuthenticated]
    # queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceReviewFilter

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        service_list = ServiceReview.objects.filter(service=service_id)
        
        
        return service_list
    
class ServiceAvailabilityCreate(generics.CreateAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, args, *kwargs):
        try:
            service = request.data.get('service', None)
            if service and Service.objects.filter(id=service).exists():
                service = Service.objects.filter(id=service)
                date = request.data.get('date', None)
                time = request.data.get('time', None)

                instance = ServiceAvailability.objects.create(service=service,
                                                              date=date,
                                                              time=time)
            else:
                return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ServiceAvailabilitySerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceAvailabilityUpdate(generics.UpdateAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, args, *kwargs):
        try:
            if Service.objects.filter(pk=kwargs['pk']).exists():
                service = ServiceAvailability.objects.get(pk=kwargs['pk'])

                date = request.data.get('date', None)
                time = request.data.get('time', None)
                if date:
                    service.date = date
                if time:
                    service.time = time

                service.save()
                serializer = ServiceAvailabilitySerializer(service)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceAvailabilityList(generics.ListAPIView):
    serializer_class = ServiceAvailabilitySerializer

    def get_queryset(self):
        service_id = self.kwargs['service']
        return ServiceAvailability.objects.filter(service__id=service_id)    
    




#vendor App 
# 
# 
# 

class ServiceAvailabeListView(generics.ListAPIView):
    serializer_class = ServiceAvailabilitySerializer

    def get_queryset(self):
        # Get the date and service ID from the URL parameters
        date_param = self.kwargs.get('date', None)
        service_id = self.kwargs.get('service_id', None)

        try:
            date_object = datetime.strptime(date_param, "%Y-%m-%d").date()
            services = ServiceAvailability.objects.filter(date=date_object, service=service_id)
            return services

        except ValueError:
            # Invalid date format
            return None

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is not None:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid date format or service ID"}, status=status.HTTP_400_BAD_REQUEST)    


# ?---------------------------App views----------------------------------------#


class ServiceTopSuggestion(generics.ListAPIView):
    """views for top suggestions & top activites"""

    queryset = Service.objects.filter(is_top_suggestion=True)
    serializer_class = ExploreMoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def get_queryset(self):
        queryset = Service.objects.all()
        
       
        service_type = self.request.query_params.get('type', None)
        if service_type:
            queryset = queryset.filter(type=service_type)
        
        return queryset    
        



class ExploreMore(generics.ListAPIView):
    """views for explore more"""

    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ExploreMoreSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter


# class NearByActivities(generics.ListAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ExploreMoreSerializer
#     filter_backends=[DjangoFilterBackend]
#     filterset_class = ServiceFilter


# class Recommendation(generics.ListAPIView):
#     queryset = Service.objects.all()
#     serializer_class = ExploreMoreSerializer
#     filter_backends = [DjangoFilterBackend]
#     flterset_class = ServiceFilter


class ServiceTypesListing(generics.ListAPIView):
    """views for all activity & service listing"""

    queryset = Service.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter


    def get_queryset(self):
        queryset = Service.objects.all()
        
       
        service_type = self.request.query_params.get('type', None)
        if service_type:
            queryset = queryset.filter(type=service_type)
        
        return queryset    
        



class CategoryBasedListing(generics.ListAPIView):
    """views for category based listing"""

    queryset = Service.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def get_queryset(self):
        category_name = self.kwargs.get("category_name")
        category = get_object_or_404(Category, name=category_name)
        return Service.objects.filter(category=category)


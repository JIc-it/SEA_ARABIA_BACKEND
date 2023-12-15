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
from local_apps.booking.models import Booking
from local_apps.booking.serializers import BookingSerializer


# vendorPrice Type Views


# class VendorPriceTypeList(generics.ListAPIView):
#     # permission_classes = [IsAuthenticated]
#     queryset = VendorPriceType.objects.all()
#     serializer_class = VendorPriceTypeSerializer


# class VendorPriceTypeCreate(generics.CreateAPIView):
#     # permission_classes = [IsAuthenticated]
#     queryset = VendorPriceType.objects.all()
#     serializer_class = VendorPriceTypeSerializer


# class VendorPriceTypeUpdate(generics.UpdateAPIView):
#     # permission_classes = [IsAuthenticated]
#     queryset = VendorPriceType.objects.all()
#     serializer_class = VendorPriceTypeSerializer


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


# vendor App
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
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "name",
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

    """View for filtering the service in service review listing section (VMS)   """
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceFilterListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name"]

    # filterset_class = ServiceFilter

    def get_queryset(self):
        user = self.request.user
        service_list = Service.objects.filter(company__user=user)
        return service_list


class ServiceFilterAdminList(generics.ListAPIView):
    """ View for filtering the service based on the company for Admin CMS   """
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceFilterListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_field = ["name"]
    filterset_class = ServiceFilter


class ServiceReviewList(generics.ListAPIView):
    """ view for showing the reviews realted to the particular service  """

    permission_classes = [IsAuthenticated]
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


# vendor App


class ServiceAvailabeListView(generics.ListAPIView):
    serializer_class = ServiceAvailabilitySerializer

    def get_queryset(self):
        # Get the date and service ID from the URL parameters
        date_param = self.kwargs.get('date', None)
        service_id = self.kwargs.get('service_id', None)

        try:
            date_object = datetime.strptime(date_param, "%Y-%m-%d").date()
            services = ServiceAvailability.objects.filter(
                date=date_object, service=service_id)
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


class AdminServiceBookingAvailabilityList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        try:
            service_id = self.kwargs.get("service")
            service = Service.objects.get(id=service_id)

            date = self.kwargs.get("date")
            if not date:
                raise ValueError("Date parameter is missing.")

            return Booking.objects.filter(service=service, start_date__date=date)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ?---------------------------App views----------------------------------------#


class ServiceTopSuggestion(generics.ListAPIView):
    """ views for top suggestions & top activites   """

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
    """ views for explore more  """

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

    # def get_queryset(self):
    #     try:
    #         user = self.request.user
    #         if user.is_authenticated:
    #             # Filter services based on bookmarks
    #             bookmarked_service_ids = Bookmark.objects.filter(user=user).values_list('service__id', flat=True)
    #             return Service.objects.filter(id__in=bookmarked_service_ids)
    #         else:
    #             return Service.objects.none()
    #     except:
    #         pass


class CategoryBasedListing(generics.ListAPIView):
    """views for category based listing"""

    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ServiceFilter

    def get_queryset(self):
        category_name = self.kwargs.get("category_name")
        category = get_object_or_404(Category, name=category_name)
        return Service.objects.filter(category=category)


class ComboPackageListing(generics.ListAPIView):
    """for combo package listing"""
    queryset = Package.objects.filter(is_active=True)
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    #  filterset_class = ServiceFilter


class ServiceAvailablityTime(generics.RetrieveAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            service_id = self.kwargs.get('pk')
            date = self.kwargs.get('date')
            service_instance = Service.objects.get(id=service_id)
            if not date:
                raise ValueError("Date Parameter is missing")
            value, _ = ServiceAvailability.objects.get_or_create(
                service=service_instance, date=date)
            serializer = self.get_serializer(value)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ServiceAvailablityTimeUpdate(generics.UpdateAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer

    def update(self, request, *args, **kwargs):
        try:
            service_id = kwargs.get('pk')
            # date = request.data.get('date')
            time = request.data.get('time')
            print(service_id, "<<<<<<")
            print(ServiceAvailability.objects.all())

            if not time:
                raise ValueError("Time Parameter is missing ")

            service_avilability = ServiceAvailability.objects.get(
                id=service_id,)
            service_avilability.time = time
            service_avilability.save()
            print(service_avilability.date, '>>>>>>')
            serializer = ServiceAvailabilitySerializer(service_avilability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)

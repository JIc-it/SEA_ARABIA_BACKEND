from django.http import HttpResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser

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
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "name",
        "amenities__name",
        "destination__name",
    ]
    filterset_class = ServiceFilter

    # def get_queryset(self):
    #     premium_category = Category.objects.filter(
    #         service_service_category__is_premium=True)
    #     return Service.objects.filter(category__in=premium_category)


class ServiceCreate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def update(self, request, *args, **kwargs):
        try:
            is_verified = request.data.get('is_verified', None)
            is_active = request.data.get('is_active', None)
            is_top_suggestion = request.data.get('is_top_suggestion', None)
            is_premium = request.data.get('is_premium', None)
            type = request.data.get('type', None)
            name = request.data.get('name', None)
            machine_id = request.data.get('machine_id', None)
            description = request.data.get('description', None)
            lounge = request.data.get('lounge', None)
            bedroom = request.data.get('bedroom', None)
            toilet = request.data.get('toilet', None)
            capacity = request.data.get('capacity', None)
            pickup_point = request.data.get('pickup_point', None)
            cancellation_policy = request.data.get('cancellation_policy', None)
            refund_policy = request.data.get('refund_policy', None)
            amenities_list = request.data.get('amenities', [])
            category = request.data.get('category', [])
            sub_category = request.data.get('sub_category', [])

            service_id = kwargs.get('pk')
            service_instance = Service.objects.get(id=service_id)

            if is_verified is not None:
                service_instance.is_verified = True if is_verified == 'true' or is_verified == 'True' or is_verified == True else False

            if is_active is not None:
                service_instance.is_active = True if is_active == 'true' or is_active == 'True' or is_active == True else False

            if is_top_suggestion is not None:
                service_instance.is_top_suggestion = True if is_top_suggestion == 'true' or is_top_suggestion == 'True' or is_top_suggestion == True else False

            if is_premium is not None:
                service_instance.is_premium = True if is_premium == 'true' or is_premium == 'True' or is_premium == True else False

            if type:
                service_instance.type = type.title()
            if name:
                service_instance.name = name
            if machine_id:
                service_instance.machine_id = machine_id
            if description:
                service_instance.description = description
            if lounge:
                service_instance.lounge = lounge
            if bedroom:
                service_instance.bedroom = bedroom
            if toilet:
                service_instance.toilet = toilet
            if capacity:
                service_instance.capacity = capacity
            if pickup_point:
                service_instance.pickup_point = pickup_point
            if cancellation_policy:
                service_instance.cancellation_policy = cancellation_policy
            if refund_policy:
                service_instance.refund_policy = refund_policy

            service_instance.save()

            if amenities_list:
                try:
                    amenities = amenities_list.replace(" ", "")
                    amenities = amenities.split(",")
                except:
                    amenities = []
                service_instance.amenities.set(amenities)

            if category:
                try:
                    category_list = category.replace(" ", "")
                    category_list = category.split(",")
                except:
                    category_list = []
                print(category_list)
                service_instance.category.set(category_list)

            if sub_category:
                try:
                    sub_category_list = sub_category.replace(" ", "")
                    sub_category_list = sub_category.split(",")
                except:
                    sub_category_list = []
                service_instance.sub_category.set(sub_category_list)

            serializer = self.get_serializer(service_instance)
            return Response(serializer.data)

        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


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


class ServiceImageCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceImageSerializer


class ServiceImageStatus(generics.UpdateAPIView):
    ''' View for updating the thumbnail status of the image '''

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceImageSerializer

    def update(self, request, *args, **kwargs):
        try:
            pk = kwargs.get('pk', None)
            service_id = request.data.get("service_id", None)

            is_thumbnail = request.data.get('is_thumbnail', None)

            serviceimage_instance = ServiceImage.objects.get(id=pk)

            thumbnail_exist = ServiceImage.objects.filter(
                service=service_id, is_thumbnail=True).exists()

            if thumbnail_exist and is_thumbnail == True:
                return Response("A thumbnail image already exist", status=status.HTTP_400_BAD_REQUEST)
            else:
                serviceimage_instance.is_thumbnail = is_thumbnail
                serviceimage_instance.save()
                return Response("Success", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ServiceImageDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            image_id = kwargs.get('pk', None)
            image_instance = ServiceImage.objects.get(id=image_id)
            image_instance.delete()
            return Response("Image deleted successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)

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
    permissionpayment_classes = [IsAuthenticated]

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
    " Service date and time availablity list view "

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
    """ Servie availablitu date and time update view """

    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer

    def update(self, request, *args, **kwargs):
        try:
            service_id = kwargs.get('pk')
            # date = request.data.get('date')
            time = request.data.get('time')

            if not time:
                raise ValueError("Time Parameter is missing ")
            service_avilability = ServiceAvailability.objects.get(
                id=service_id,)
            service_avilability.time = time
            service_avilability.save()
            serializer = ServiceAvailabilitySerializer(service_avilability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ServiceListApp(generics.ListAPIView):
    """for app side service lisiting"""

    queryset = Service.objects.all()
    premium_category = Category.objects.filter(
        service_service_category__is_premium=True)
    serializer_class = ServiceSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "name",
        "amenities__name",
        "destination__name",
    ]
    filterset_class = ServiceFilter


# Export

class ExportServiceCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Service.objects.all()
        resource = ServiceListExportResource()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="service_list.csv"'

        return response

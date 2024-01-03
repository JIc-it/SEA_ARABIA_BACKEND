from django.db.models import Q
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
from datetime import datetime, timedelta
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
    permission_classes = [IsAuthenticated]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def create(self, request, *args, **kwargs):
        try:

            service_prices = request.data.pop('service_price_service', [])
            amenities_list = request.data.pop('amenities', None)
            category = request.data.pop('category', None)
            sub_category = request.data.pop('sub_category', [])
            profit_id = request.data.pop('profit_method', None)
            price_id = request.data.pop('price_type', None)
            company_id = request.data.pop('company', None)

            company_instance = Company.objects.get(id=company_id)
            profit_instance = ProfitMethod.objects.get(id=profit_id)
            price_instance = PriceType.objects.get(id=price_id)

            service_instance = Service.objects.create(
                company=company_instance, profit_method=profit_instance, price_type=price_instance, **request.data)

            if category:
                service_instance.category.add(category)

            if sub_category:
                service_instance.sub_category.add(sub_category)

            if amenities_list:
                try:
                    amenities = amenities_list.replace(" ", "")
                    amenities = amenities.split(",")
                except:
                    amenities = []
                service_instance.amenities.set(amenities)

            for service_price in service_prices:
                """ creating service prices """

                price_id = service_price.get('id', None)
                is_active = service_price.get('is_active', None)
                name = service_price.get('name', None)
                price = service_price.get('price', None)
                is_range = service_price.get('is_range', None)
                location = service_price.pop('location', None)
                duration_hour = service_price.get('duration_hour', None)
                duration_minute = service_price.get('duration_minute', None)
                duration_day = service_price.get('duration_day', None)
                end_time = service_price.get('end_time', None)
                time = service_price.get('time', None)
                day = service_price.get('day', None)
                end_day = service_price.get('end_day', None)
                date = service_price.get('date', None)
                end_date = service_price.get('end_date', None)

                if location:
                    location_instance = Destination.objects.get(id=location)

                Price.objects.create(
                    **service_price, service=service_instance, location=location_instance)

            serializer = self.get_serializer(service_instance)
            return Response(serializer.data)

        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


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
            is_recommended = request.data.get('is_recommended', None)
            is_sail_with_activity = request.data.get(
                'is_sail_with_activity', None)
            types = request.data.get('type', None)
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
            is_duration = request.data.get('is_duration', None)
            is_date = request.data.get('is_date', None)
            is_day = request.data.get('is_day', None)
            is_time = request.data.get('is_time', None)
            is_destination = request.data.get('is_destination', None)
            price_type = request.data.get('price_type', None)
            profit_method = request.data.get('profit_method', None)
            vendor_percentage = request.data.get('vendor_percentage', None)
            sea_arabia_percentage = request.data.get(
                'sea_arabia_percentage', None)
            markup_fee = request.data.get('markup_fee', None)
            per_head_booking = request.data.get('per_head_booking', None)
            purchase_limit_min = request.data.get('purchase_limit_min', None)
            purchase_limit_max = request.data.get('purchase_limit_max', None)

            service_prices = request.data.get('service_price_service', [])

            amenities_list = request.data.get('amenities', None)
            category = request.data.get('category', [])
            sub_category = request.data.get('sub_category', [])

            service_id = kwargs.get('pk')
            service_instance = Service.objects.get(id=service_id)

            if is_verified is not None:
                service_instance.is_verified = True if is_verified == 'true' or is_verified == 'True' or is_verified == True else False

            if per_head_booking is not None:
                service_instance.per_head_booking = True if per_head_booking == 'true' or per_head_booking == 'True' or per_head_booking == True else False

            if is_recommended is not None:
                service_instance.is_recommended = True if is_recommended == 'true' or is_recommended == 'True' or is_recommended == True else False

            if is_active is not None:
                service_instance.is_active = True if is_active == 'true' or is_active == 'True' or is_active == True else False

            if is_top_suggestion is not None:
                service_instance.is_top_suggestion = True if is_top_suggestion == 'true' or is_top_suggestion == 'True' or is_top_suggestion == True else False

            if is_premium is not None:
                service_instance.is_premium = True if is_premium == 'true' or is_premium == 'True' or is_premium == True else False

            if is_sail_with_activity is not None:
                service_instance.is_sail_with_activity = True if is_sail_with_activity == 'true' or is_sail_with_activity == 'True' or is_sail_with_activity == True else False

            if is_duration is not None:
                service_instance.is_duration = True if is_duration == 'true' or is_duration == 'True' or is_duration == True else False

            if is_date is not None:
                service_instance.is_date = True if is_date == 'true' or is_date == 'True' or is_date == True else False

            if is_day is not None:
                service_instance.is_day = True if is_day == 'true' or is_day == 'True' or is_day == True else False

            if is_time is not None:
                service_instance.is_time = True if is_time == 'true' or is_time == 'True' or is_time == True else False

            if is_destination is not None:
                service_instance.is_destination = True if is_destination == 'true' or is_destination == 'True' or is_destination == True else False

            if types:
                service_instance.type = types.title()
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
            if vendor_percentage:
                service_instance.vendor_percentage = vendor_percentage
            if sea_arabia_percentage:
                service_instance.sea_arabia_percentage = sea_arabia_percentage
            if markup_fee:
                service_instance.markup_fee = markup_fee
            if purchase_limit_min:
                service_instance.purchase_limit_min = purchase_limit_min
            if purchase_limit_max:
                service_instance.purchase_limit_max = purchase_limit_max

            if profit_method:
                profit_method_instance = ProfitMethod.objects.get(
                    id=profit_method)
                service_instance.profit_method = profit_method_instance
            if price_type:
                price_type_instance = PriceType.objects.get(id=price_type)
                service_instance.price_type = price_type_instance

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

            for service_price in service_prices:
                """ updating the service prices """

                price_id = service_price.get('id', None)
                is_active = service_price.get('is_active', None)
                service_name = service_price.get('name', None)
                price = service_price.get('price', None)
                is_range = service_price.get('is_range', None)
                location = service_price.pop('location', None)
                duration_hour = service_price.get('duration_hour', None)
                duration_minute = service_price.get('duration_minute', None)
                duration_day = service_price.get('duration_day', None)
                end_time = service_price.get('end_time', None)
                time = service_price.get('time', None)
                day = service_price.get('day', None)
                end_day = service_price.get('end_day', None)
                date = service_price.get('date', None)
                end_date = service_price.get('end_date', None)

                if price_id:
                    price_instance = Price.objects.get(id=price_id)

                    if is_active is not None:
                        price_instance.is_active = True if is_active == 'true' or is_active == 'True' or is_active == True else False

                    if is_range is not None:
                        price_instance.is_range = True if is_range == 'true' or is_range == 'True' or is_range == True else False

                    if service_name:
                        price_instance.name = service_name
                    if price:
                        price_instance.price = price
                    if location:
                        location_instance = Destination.objects.get(
                            id=location)
                        price_instance.location = location_instance
                    if duration_hour:
                        price_instance.duration_hour = duration_hour
                    if duration_minute:
                        price_instance.duration_minute = duration_minute
                    if duration_day:
                        price_instance.duration_day = duration_day
                    if end_time:
                        price_instance.endtime = end_time
                    if time:
                        price_instance.time = time
                    if day:
                        price_instance.day = day.title()
                    if end_day:
                        price_instance.end_day = end_day.title()
                    if date:
                        price_instance.date = date
                    if end_date:
                        price_instance.end_date = end_date

                    price_instance.save()

                else:
                    if location:
                        location_instance = Destination.objects.get(
                            id=location)
                        Price.objects.create(
                            service=service_instance, location=location_instance, **service_price)
                    else:
                        Price.objects.create(
                            service=service_instance, **service_price)

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
    search_fields = ["name"]
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


# class ServiceAvailabilityCreate(generics.CreateAPIView):
#     queryset = ServiceAvailability.objects.all()
#     serializer_class = ServiceAvailabilitySerializer
#     permission_classes = [IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         try:
#             service_id = request.data.get('service', None)
#             if service_id and Service.objects.filter(id=service_id).exists():
#                 service_instance = Service.objects.get(id=service_id)
#                 date = request.data.get('date', None)
#                 time = request.data.get('time', None)
#                 all_slots_available = request.data.get('all', None)
#
#                 instance = ServiceAvailability.objects.create(service=service_instance,
#                                                               date=date,
#                                                               time=time,
#                                                               all_slots_available=all_slots_available)
#             else:
#                 return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)
#
#             serializer = ServiceAvailabilitySerializer(instance)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ServiceAvailabilityCreate(generics.CreateAPIView):
    queryset = ServiceAvailability.objects.all()
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            service_id = request.data.get('service', None)
            if service_id and Service.objects.filter(id=service_id).exists():
                service_instance = Service.objects.get(id=service_id)
                date = request.data.get('date', None)
                time = request.data.get('time', None)

                # Determine the availability based on provided time or use default_false_time_slot
                if time is not None:
                    all_slots_available = [
                        {'time': i, 'make_slot_available': (i == int(time))} for i in range(24)
                    ]
                else:
                    all_slots_available = default_true_time_slot()

                instance = ServiceAvailability.objects.create(
                    service=service_instance,
                    date=date,
                    time=time,
                    all_slots_available=all_slots_available
                )
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
                all = request.data.get('all', None)
                if date:
                    service.date = date
                if time:
                    service.time = time
                if all:
                    service.all_slots_available = all

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
        date_or_month_param = self.kwargs.get('date_or_month', None)
        service_id = self.kwargs.get('service_id', None)

        try:
            # Attempt to parse as date, if fails, assume it's a year-month parameter
            try:
                date_object = datetime.strptime(
                    date_or_month_param, "%Y-%m-%d").date()
                services = ServiceAvailability.objects.filter(
                    date=date_object, service=service_id)
            except ValueError:
                year, month = map(int, date_or_month_param.split('-'))
                services = ServiceAvailability.objects.filter(
                    Q(date__year=year, date__month=month) | Q(date__isnull=True),
                    service=service_id
                )

        except (ValueError, IndexError) as e:
            # Print the exception details for debugging
            print(f"Error: {e}")
            return ServiceAvailability.objects.none()

        return services

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No services available for the given criteria"},
                            status=status.HTTP_404_NOT_FOUND)


class AdminServiceBookingAvailabilityList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        try:
            service_id = self.kwargs.get("service")
            service = Service.objects.get(id=service_id)

            date = self.kwargs.get("date")
            month = self.kwargs.get("month")
            if not date:
                raise ValueError("Date parameter is missing.")
            if not month:
                raise ValueError("Month parameter is missing.")

            return Booking.objects.filter(service=service, start_date__date=date,
                                          start_date__month=month)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ?---------------------------App views----------------------------------------#


class ServiceTopSuggestion(generics.ListAPIView):
    """ views for top suggestions & top activites   """

    queryset = Service.objects.filter(is_top_suggestion=True)
    serializer_class = ServiceSerializer
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
    serializer_class = ServiceSerializer
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
                id=service_id, )
            service_avilability.time = time
            service_avilability.save()
            serializer = ServiceAvailabilitySerializer(service_avilability)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class ServiceListApp(generics.ListAPIView):
    """ for app side service lisiting """

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


# service review views


class ServiceReviewCreate(generics.CreateAPIView):
    """for app side review creation"""
    serializer_class = ServiceReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        service_id = self.kwargs.get(
            'service_id') or request.data.get('service')

        if Booking.objects.filter(user=request.user, service_id=service_id).exists():
            booking = Booking.objects.get(
                user=request.user, service_id=service_id)

            if booking.status == 'Completed':

                if not ServiceReview.objects.filter(user=request.user, service_id=service_id).exists():

                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(user=request.user, service_id=service_id)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "You have already reviewed this service."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Service not completed yet."}, status=status.HTTP_400_BAD_REQUEST)
        else:

            return Response({"message": "You have not booked this service yet."}, status=status.HTTP_400_BAD_REQUEST)


class ServiceReviewListApp(generics.ListAPIView):
    """view for review"""
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        service_id = self.kwargs.get("pk")
        service_list = ServiceReview.objects.filter(service=service_id)

        return service_list


class ServiceReviewUpdate(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = ServiceReview.objects.all()
    serializer_class = ServiceReviewSerializer


class ProfitMethodList(generics.ListAPIView):
    """ view for listing the Profit Method"""

    permission_classes = [IsAuthenticated]
    queryset = ProfitMethod.objects.all()
    serializer_class = ProfitMethodSerializer


class PriceTypeList(generics.ListAPIView):
    """ view for listing the Price Type"""

    permission_classes = [IsAuthenticated]
    queryset = PriceType.objects.all()
    serializer_class = PriceTypeSerializer


class PackageCreateAPIView(generics.CreateAPIView):
    """for cms side"""
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter

    def perform_create(self, serializer):
        serializer.save()


class PackageUpdateAPIView(generics.UpdateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class PackagDeleteAPIView(generics.DestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    lookup_field = 'pk'


class PackageListAPIView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PackageFilter


# class UpdateAvailabilityView(generics.UpdateAPIView):
#     serializer_class = ServiceAvailabilitySerializer
#
#     def update(self, request, *args, **kwargs):
#         service_id = kwargs['service']
#         update_type = request.query_params.get('update_type', None)
#
#         # Retrieve the Service instance based on the provided UUID
#         service_instance = Service.objects.get(id=service_id)
#
#         date_str = self.kwargs.get('date')
#         try:
#             date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
#         except ValueError:
#             return Response({"error": f"Invalid date format for {date_str}. "
#                                       f"Use DD-MM-YYYY."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Use get_or_create to retrieve or create the ServiceAvailability instance
#         service_availability_instance, created = (ServiceAvailability.objects.get_or_create
#                                                   (service=service_instance, date=date_obj))
#
#         if update_type == 'all':
#             # Handle by_duration logic
#             date_str = self.kwargs.get('date')
#             try:
#                 date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
#             except ValueError:
#                 return Response({"error": f"Invalid date format for {date_str}. "
#                                           f"Use DD-MM-YYYY."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             try:
#                 service_availability_instance = (ServiceAvailability.objects.get
#                                                  (service=service_instance, date=date_obj))
#             except ServiceAvailability.DoesNotExist:
#                 return Response({"error": f"Service availability not found for "
#                                           f"{date_str}."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             service_availability_instance.time = default_true_time_slot()
#             service_availability_instance.all_slots_available = True
#             service_availability_instance.save()
#
#         elif update_type == 'time':
#             # Handle by_time logic
#             time = int(request.query_params.get('time', 0))
#             date_str = self.kwargs.get('date')
#             try:
#                 date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
#             except ValueError:
#                 return Response({"error": f"Invalid date format for {date_str}. "
#                                           f"Use DD-MM-YYYY."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             try:
#                 service_availability_instance = (ServiceAvailability.objects.get
#                                                  (service=service_instance, date=date_obj))
#             except ServiceAvailability.DoesNotExist:
#                 return Response({"error": f"Service availability not found for "
#                                           f"{date_str}."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             # Update the availability for the specific time
#             for slot in service_availability_instance.time:
#                 if slot['time'] == time:
#                     slot['make_slot_available'] = True
#
#             service_availability_instance.save()
#
#         elif update_type == 'date':
#             # Handle by_duration logic
#             date_str = self.kwargs.get('date')
#             try:
#                 date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
#             except ValueError:
#                 return Response({"error": f"Invalid date format for {date_str}. "
#                                           f"Use DD-MM-YYYY."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             try:
#                 service_availability_instance = (ServiceAvailability.objects.get
#                                                  (service=service_instance, date=date_obj))
#             except ServiceAvailability.DoesNotExist:
#                 return Response({"error": f"Service availability not found for "
#                                           f"{date_str}."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             service_availability_instance.time = default_true_time_slot()
#             service_availability_instance.all_slots_available = True
#             service_availability_instance.save()
#
#         else:
#             return Response({"error": "Invalid update_type"},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({"message": "Availability updated successfully"},
#                         status=status.HTTP_201_CREATED)


class UpdateAvailabilityView(generics.UpdateAPIView):
    serializer_class = ServiceAvailabilitySerializer

    def update(self, request, *args, **kwargs):
        service_id = kwargs['service']
        update_type = request.query_params.get('update_type', None)

        # Retrieve the Service instance based on the provided UUID
        service_instance = Service.objects.get(id=service_id)

        date_str = self.kwargs.get('date')
        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
        except ValueError:
            return Response({"error": f"Invalid date format for {date_str}. "
                                      f"Use DD-MM-YYYY."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Use get_or_create to retrieve or create the ServiceAvailability instance
        service_availability_instance, created = ServiceAvailability.objects.get_or_create(
            service=service_instance,
            date=date_obj
        )

        if update_type == 'all':
            # Handle by_duration logic
            service_availability_instance.time = default_true_time_slot()
            service_availability_instance.all_slots_available = True
            service_availability_instance.save()

        elif update_type == 'time':
            # Handle by_time logic
            time = int(request.query_params.get('time', 0))
            # Update the availability for the specific time
            for slot in service_availability_instance.time:
                if slot['time'] == time:
                    slot['make_slot_available'] = True
            service_availability_instance.save()

        elif update_type == 'date':
            # Handle by_duration logic
            service_availability_instance.time = default_true_time_slot()
            service_availability_instance.all_slots_available = True
            service_availability_instance.save()

        elif update_type == 'days':
            # Handle by_days logic
            selected_days = request.data.get('days', [])
            selected_days = set(selected_days)

            # Find the nearest dates that match the selected days
            nearest_dates = []
            current_date = date_obj
            while len(nearest_dates) < len(selected_days):
                if current_date.strftime('%A').lower() in selected_days:
                    nearest_dates.append(current_date)
                current_date += timedelta(days=1)

            # Update availability for the nearest dates
            for nearest_date in nearest_dates:
                service_availability_instance, _ = ServiceAvailability.objects.get_or_create(
                    service=service_instance,
                    date=nearest_date
                )
                # Assuming days_available is a list of days
                for day in selected_days:
                    if day in service_availability_instance.days_available:
                        # Update the availability for the specific day
                        service_availability_instance.days_available[day] = True

                service_availability_instance.save()

        else:
            return Response({"error": "Invalid update_type"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Availability updated successfully"},
                        status=status.HTTP_201_CREATED)


class ServiceIndividualView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceIndividualSerializer


class ServicePriceDelete(generics.DestroyAPIView):
    serializer_class = PriceSerializer
    queryset = Price.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Price object deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

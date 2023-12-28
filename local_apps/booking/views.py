from rest_framework import generics, status
from .models import Booking, Payment
from .serializers import *
from rest_framework.response import Response
from local_apps.service.models import Service
from local_apps.offer.models import Offer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework import status
from django.db.models import Case, Count, Q, Sum, IntegerField, When
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
import datetime
from .filters import *
from django.http import HttpResponse


today = datetime.date.today()


class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "booking_id",
        "service__name",
        "user__first_name",
        "user__last_name"
    ]
    filterset_class = BookingFilter


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            offer_id = request.data.get('offer')
            service_id = request.data.get('service')
            payment_id = request.data.get('payment')

            # Get related objects
            offer = Offer.objects.get(id=offer_id) if offer_id else None
            service = Service.objects.get(id=service_id) if service_id else None
            payment = Payment.objects.get(id=payment_id) if payment_id else None

            # Extract JSON fields
            user_details = request.data.get('user_details', {})
            guest_details = request.data.get('guest_details', {})
            service_details = request.data.get('service_details', {})
            price_details = request.data.get('price_details', {})
            offer_details = request.data.get('offer_details', {})

            # Create Booking instance
            booking = Booking(
                user=request.user,
                offer=offer,
                service=service,
                payment=payment,
                for_myself=request.data.get('for_myself'),
                for_someone_else=request.data.get('for_someone_else'),
                first_name=request.data.get('first_name'),
                last_name=request.data.get('last_name'),
                phone_number=request.data.get('phone_number'),
                email=request.data.get('email'),
                user_type=request.data.get('user_type'),
                starting_point=request.data.get('starting_point'),
                destination=request.data.get('destination'),
                start_date=request.data.get('start_date'),
                end_date=request.data.get('end_date'),
                slot_details=request.data.get('slot_details'),
                additional_hours=request.data.get('additional_hours', 0),
                additional_hours_amount=request.data.get('additional_hours_amount', 0),
                number_of_people=request.data.get('number_of_people', 1),
                status=request.data.get('status', 'Opened'),
                booking_type=request.data.get('booking_type', 'Booking'),
                cancellation_reason=request.data.get('cancellation_reason'),
                refund_status=request.data.get('refund_status'),
                refund_type=request.data.get('refund_type'),
                refund_amount=request.data.get('refund_amount'),
                refund_details=request.data.get('refund_details'),
                price_total=request.data.get('price_total', 0),
                user_details=user_details,
                guest_details=guest_details,
                service_details=service_details,
                price_details=price_details,
                package_details=request.data.get('package_details', {}),
                offer_details=offer_details
            )

            booking.save()

            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class BookingCardCount(APIView):
    """ Booking card count for admin cms """

    def get(self, request):
        """ Passing id of the vendor will give the count of the booking for the particular vendor only 
        else return the total count of bookings """

        try:
            vendor_id = request.query_params.get('id', None)

            if vendor_id:
                booking_count = Booking.objects.filter(service__company__user=vendor_id).aggregate(
                    total_booking=Count("pk"),
                    today_booking=Coalesce(Sum(
                        Case(When(created_at=today, then=1), default=0, output_field=IntegerField())), 0),
                    total_confirmed_booking=Coalesce(Sum(
                        Case(When(status="Successful", then=1), default=0, output_field=IntegerField())), 0),
                    total_cancelled_booking=Coalesce(Sum(
                        Case(When(status="Cancelled", then=1), default=0, output_field=IntegerField())), 0),
                )
            else:
                booking_count = Booking.objects.all().aggregate(
                    total_booking=Count("pk"),
                    today_booking=Coalesce(Sum(
                        Case(When(created_at=today, then=1), default=0, output_field=IntegerField())), 0),
                    total_confirmed_booking=Coalesce(Sum(
                        Case(When(status="Successful", then=1), default=0, output_field=IntegerField())), 0),
                    total_cancelled_booking=Coalesce(Sum(
                        Case(When(status="Cancelled", then=1), default=0, output_field=IntegerField())), 0),
                )

            return Response(booking_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error:{str(e)}", status=status.HTTP_400_BAD_REQUEST)


class BookingStatusUpdate(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            booking_status = request.data.get('status')
            booking_id = kwargs.get('pk', None)

            booking_instance = get_object_or_404(Booking, id=booking_id)
            if booking_status:
                booking_instance.status = booking_status.title()
                booking_instance.save()
            return Response({"Booking Status": booking_instance.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error : {str(e)}", status=status.HTTP_400_BAD_REQUEST)


# ?---------------------------App views----------------------------------------#


class BookingAppList(generics.ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "booking_id",
        "service__name",
        "user__first_name",
        "user__last_name"
    ]
    filterset_class = BookingFilter

    def get_queryset(self):

        return Booking.objects.filter(user=self.request.user)


# Export as CSV

class ExportBookingCSVView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Booking.objects.all()
        resource = BookingListExport()

        dataset = resource.export(queryset)

        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings_list.csv"'

        return response

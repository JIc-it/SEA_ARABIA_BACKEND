from rest_framework import generics, status
from .serializers import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from django.db.models import Case, Count, Sum, IntegerField, When
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
import datetime
from .filters import *
from .resources import BookingResource
from django.http import HttpResponse

today = datetime.date.today()

# vendor Side List


class AdminBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "booking_id",
        "service__name",
        "user__first_name",
        "user__last_name"
    ]
    filterset_class = BookingFilter


class AdminIndividualBookingView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            booking_id = self.request.data.get('booking_id', None)
            if booking_id is None:
                raise ValueError("Booking ID is required.")

            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if isinstance(instance, Response):
            return instance

        serializer = self.get_serializer(instance)
        return Response(serializer.data)   


class VendorBookingListView(generics.ListAPIView):
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
        try:
            return Booking.objects.filter(service__company__user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserBookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.all()
        try:
            return Booking.objects.filter(user=self.request.user)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     # Save the current booking
    #     instance = serializer.save()
    #     print('hello working')
    #     # Perform additional actions after saving the booking
    #     # For example, you can call a method on the instance or perform other operations
    #     instance.your_custom_method()

    #     # You can also perform actions on related models or any other logic you need
    #     # ...

    #     # Finally, return the instance
    #     return instance


class BookingView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class BookingStatusUpdate(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            booking_status = request.data.get('status', None)
            allowed_statuses = [data[0] for data in Booking.BOOKING_STATUS]
            if booking_status not in allowed_statuses:
                raise serializers.ValidationError(
                    f"Invalid booking status. Allowed statuses are: {', '.join(allowed_statuses)}")
            booking_id = kwargs.get('pk', None)
            booking_instance = get_object_or_404(Booking, id=booking_id)
            if booking_status:
                booking_instance.status = booking_status if booking_status else None
                booking_instance.save()
            return Response({"message": f"Booking status changes : {booking_instance.status}"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error : {str(e)}", status=status.HTTP_400_BAD_REQUEST)


class AdminBookingCardCount(APIView):
    """ Booking card count for admin cms """

    def get(self, request):
        """ fetching the count of all booking """
        try:

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


class ExportBooking(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Booking.objects.all()
        resource = BookingResource()
        dataset = resource.export(queryset)
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="bookings_list.csv"'
        return response


class BookingCancellation(generics.UpdateAPIView):
    serializer_class = BookingStatusSerializer
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            booking_id = kwargs.get('pk', None)
            cancellation_reason = request.data.get('cancellation_reason')
            booking_instance = Booking.objects.get(
                id=booking_id) if Booking.objects.filter(id=booking_id).exists() else None

            if booking_instance and booking_instance.status != 'Cancelled':
                booking_instance.cancelled_by = self.request.user
                booking_instance.status = 'Cancelled'
                booking_instance.cancellation_reason = cancellation_reason
                booking_instance.refund_status = 'Pending'
                booking_instance.save()
            else:
                return Response({"error": "Booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"Booking Status": booking_instance.status}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentFinalization(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            payment_id = request.data.get("payment_id")

        except Exception as e:
            return Response(f'Error {str(e)}', status=status.HTTP_400_BAD_REQUEST)


class VendorBookingCardCount(APIView):
    def get(self, request):
        """ passing the vendor id retrive the count of booking associated with the vendor only  """

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
                return Response(booking_count, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error {str(e)}", status=status.HTTP_400_BAD_REQUEST)

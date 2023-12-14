from rest_framework import generics, status
from .models import Booking, Payment
from .serializers import BookingSerializer
from rest_framework.response import Response
from local_apps.service.models import Service
from local_apps.offer.models import Offer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import *


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
            offer = request.data.get('offer', None)
            service = request.data.get('service', False)
            payment = request.data.get('payment', False)
            user_type = request.data.get('user_type', False)
            starting_point = request.data.get('starting_point', False)
            destination = request.data.get('destination', False)
            start_date = request.data.get('start_date', False)
            end_date = request.data.get('end_date', False)
            slot = request.data.get('slot', False)
            additional_hours = request.data.get('additional_hours', False)
            additional_hours_amount = request.data.get(
                'additional_hours_amount', False)
            adults = request.data.get('adults', False)
            children = request.data.get('children', False)
            is_insured = request.data.get('is_insured', False)
            insurance_id = request.data.get('insurance_id', False)
            booking_status = request.data.get('status', False)

            try:
                service = Service.objects.get(id=service)
            except Service.DoesNotExist:
                service = None

            try:
                payment = Payment.objects.get(id=payment)
            except Payment.DoesNotExist:
                payment = None

            try:
                offer = Offer.objects.get(id=offer)
            except Offer.DoesNotExist:
                offer = None

            booking = Booking.objects.create(
                user=request.user,
                offer=offer,
                service=service,
                payment=payment,
                user_type=user_type,
                starting_point=starting_point,
                destination=destination,
                start_date=start_date,
                end_date=end_date,
                slot=slot,
                additional_hours=additional_hours,
                additional_hours_amount=additional_hours_amount,
                adults=adults,
                children=children,
                is_insured=is_insured,
                insurance_id=insurance_id,
                status=booking_status)
            booking.save()
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookingView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Offers, Booking, PassengerDetails
from .serializers import OffersSerializer, BookingSerializer, PassengerDetailsSerializer

class OffersList(generics.ListCreateAPIView):
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer

class OffersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer

class PassengerDetailsList(generics.ListCreateAPIView):
    queryset = PassengerDetails.objects.all()
    serializer_class = PassengerDetailsSerializer

class PassengerDetailsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PassengerDetails.objects.all()
    serializer_class = PassengerDetailsSerializer

class BookingList(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

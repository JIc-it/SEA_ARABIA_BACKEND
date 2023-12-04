# serializers.py

from rest_framework import serializers
from .models import Offers, Booking, PassengerDetails

class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'

class PassengerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetails
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    passenger_details = PassengerDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'

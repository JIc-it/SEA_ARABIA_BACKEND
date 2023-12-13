from rest_framework import serializers
from .models import Booking, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id',
                  'status']


class BookingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(allow_null=True, required=False)

    class Meta:
        model = Booking
        fields = ['booking_id',
                  'user',
                  'offer',
                  'service',
                  'payment',
                  'user_type',
                  'starting_point',
                  'destination',
                  'start_date',
                  'end_date',
                  'slot',
                  'additional_hours',
                  'additional_hours_amount',
                  'adults',
                  'children',
                  'is_insured',
                  'insurance_id',
                  'status']

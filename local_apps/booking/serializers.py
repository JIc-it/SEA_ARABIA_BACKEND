from rest_framework import serializers
from .models import Booking, Payment
from local_apps.service.serializers import ServiceSerializer
from local_apps.offer.serializers import OfferSerializer
from local_apps.account.serializers import UserSerializer
from import_export import resources


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id',
                  'status']


class BookingSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(allow_null=True, required=False)
    service = ServiceSerializer(allow_null=True, required=False)
    offer = OfferSerializer(allow_null=True, required=False)
    user = UserSerializer(allow_null=True, required=False)

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


class BookingStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class BookingListExport(resources.ModelResource):
    service = resources.Field(column_name='service', attribute='service__name')
    category = resources.Field(column_name='category', attribute='service__category__name')
    vendor = resources.Field(column_name='vendor', attribute='service__company__name')
    user = resources.Field(column_name='user', attribute='user__first_name')

    class Meta:
        model = Booking
        fields = ['booking_id',
                  'service',
                  'category',
                  'vendor',
                  'user',
                  'user_type',
                  'end_date',
                  'created_at',
                  # 'start_date',
                  'status']

        export_order = fields

    


    

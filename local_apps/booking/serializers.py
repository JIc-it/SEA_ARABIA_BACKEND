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
                  'guest',
                  'offer',
                  'service',
                  'payment',
                  'package',
                  'price',
                  'user_type',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'email',
                  'for_myself',
                  'for_someone_else',
                  'booking_for',
                  'booking_item',
                  'starting_point',
                  'destination',
                  'start_date',
                  'end_date',
                  'slot_details',
                  'additional_hours',
                  'additional_hours_amount',
                  'number_of_people',
                  'status',
                  'booking_type',
                  'cancellation_reason',
                  'refund_status',
                  'refund_type',
                  'refund_amount',
                  'refund_details',
                  'price_total',
                  'user_details',
                  'guest_details',
                  'service_details',
                  'price_details',
                  ]


class BookingStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class BookingListExport(resources.ModelResource):
    service = resources.Field(column_name='service', attribute='service__name')
    category = resources.Field(column_name='category', attribute='service__categories')
    vendor = resources.Field(column_name='vendor', attribute='service__company__name')
    user = resources.Field(column_name='user', attribute='user__first_name')

    def dehydrate_category(self, booking):
        return ', '.join(category.name for category in booking.service.category.all())

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
                  'status']

        export_order = fields


    


    

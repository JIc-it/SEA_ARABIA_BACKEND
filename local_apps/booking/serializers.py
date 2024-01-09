from rest_framework import serializers
from local_apps.service.models import Package, Price, Service
from local_apps.offer.models import Offer

from local_apps.account.models import Guest, User
from .models import Booking, Payment
from local_apps.service.serializers import ServiceSerializer, PackageSerializer, PriceSerializer
from local_apps.offer.serializers import OfferSerializer
from local_apps.account.serializers import UserSerializer, GuestSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id',
                  'payment_id',
                  'tap_pay_id',
                  'amount',
                  'status',
                  'payment_method',
                  'initial_response',
                  'confirmation_response',
                  'created_at',
                  'updated_at',
                  "payment_response_message",]


class BookingSerializer(serializers.ModelSerializer):
    # Ladders for extra details
    user = UserSerializer(allow_null=True, required=False)
    guest = GuestSerializer(allow_null=True, required=False)
    offer = OfferSerializer(allow_null=True, required=False)
    service = ServiceSerializer(allow_null=True, required=False)
    payment = PaymentSerializer(allow_null=True, required=False)
    package = PackageSerializer(allow_null=True, required=False)
    price = PriceSerializer(allow_null=True, required=False)
    payment_url = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Booking
        fields = ['id',
                  "booking_id",
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
                  'destination',
                  'booking_for',
                  'booking_item',
                  'starting_point',
                  'start_date',
                  'end_date',
                  'slot_details',
                  'additional_hours',
                  'additional_hours_amount',
                  'number_of_people',
                  'booking_type',
                  'status',
                  'cancellation_reason',
                  'cancelled_by',
                  'refund_status',
                  'cancelled_date',
                  'is_refunded',
                  'refund_type',
                  'refund_amount',
                  'refund_details',
                  'price_total',
                  'created_at',
                  'updated_at',
                  "payment_url",
                  "user_id"
                  ]

    def create(self, validated_data):
        # Extract UUIDs from validated data
        user_uuid = validated_data.pop('user', None)
        guest_uuid = validated_data.pop('guest', None)
        offer_uuid = validated_data.pop('offer', None)
        service_uuid = validated_data.pop('service', None)
        payment_uuid = validated_data.pop('payment', None)
        package_uuid = validated_data.pop('package', None)
        price_uuid = validated_data.pop('price', None)

        # Retrieve related instances
        user = User.objects.get(id=user_uuid) if user_uuid else None
        guest = Guest.objects.get(id=guest_uuid) if guest_uuid else None
        offer = Offer.objects.get(id=offer_uuid) if offer_uuid else None
        service = Service.objects.get(id=service_uuid) if service_uuid else None
        payment = Payment.objects.get(id=payment_uuid) if payment_uuid else None
        package = Package.objects.get(id=package_uuid) if package_uuid else None
        price = Price.objects.get(id=price_uuid) if price_uuid else None

        # Update validated data with related instances
        validated_data['user'] = user
        validated_data['guest'] = guest
        validated_data['offer'] = offer
        validated_data['service'] = service
        validated_data['payment'] = payment
        validated_data['package'] = package
        validated_data['price'] = price

        # Create Booking instance
        booking = Booking.objects.create(**validated_data)

        return booking

    # @staticmethod
    # def validate_user_type(self, value):
    #     allowed_user_types = [data[0] for data in Booking.USER_TYPE]
    #     if value not in allowed_user_types:
    #         raise serializers.ValidationError(f"Invalid user type. Allowed types are: {', '.join(allowed_user_types)}")
    #     return value

    # @staticmethod
    # def validate_booking_for(self, value):
    #     allowed_booking_for = [data[0] for data in Booking.BOOKING_FOR_TYPE]
    #     if value not in allowed_booking_for:
    #         raise serializers.ValidationError(
    #             f"Invalid booking for. Allowed options are: {', '.join(allowed_booking_for)}")
    #     return value

    # @staticmethod
    # def validate_booking_item(self, value):
    #     allowed_booking_item = [data[0] for data in Booking.BOOKING_ITEM_TYPE]
    #     if value not in allowed_booking_item:
    #         raise serializers.ValidationError(
    #             f"Invalid booking item. Allowed items are: {', '.join(allowed_booking_item)}")
    #     return value

    # @staticmethod
    # def validate_booking_type(self, value):
    #     allowed_booking_type = [data[0] for data in Booking.BOOKING_CHOICE]
    #     if value not in allowed_booking_type:
    #         raise serializers.ValidationError(
    #             f"Invalid booking type. Allowed types are: {', '.join(allowed_booking_type)}")
    #     return value

    # @staticmethod
    # def validate_status(self, value):
    #     allowed_statuses = [data[0] for data in Booking.BOOKING_STATUS]
    #     if value not in allowed_statuses:
    #         raise serializers.ValidationError(
    #             f"Invalid booking status. Allowed statuses are: {', '.join(allowed_statuses)}")
    #     return value

    # @staticmethod
    # def validate_refund_status(self, value):
    #     allowed_refund_statuses = [data[0] for data in Booking.REFUND_STATUS]
    #     if value not in allowed_refund_statuses:
    #         raise serializers.ValidationError(
    #             f"Invalid refund status. Allowed statuses are: {', '.join(allowed_refund_statuses)}")
    #     return value

    # @staticmethod
    # def validate_refund_type(self, value):
    #     allowed_refund_types = [data[0] for data in Booking.REFUND_TYPE]
    #     if value not in allowed_refund_types:
    #         raise serializers.ValidationError(
    #             f"Invalid refund type. Allowed types are: {', '.join(allowed_refund_types)}")
    #     return value


class BookingStatusSerializer(serializers.Serializer):
    status = serializers.CharField()

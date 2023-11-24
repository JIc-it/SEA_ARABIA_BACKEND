from rest_framework import serializers
from .models import *


class OccassionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occasion
        exclude = ["created_at", "updated_at"]


class VendorPriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPriceType
        exclude = ["created_at", "updated_at"]


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        exclude = ["created_at", "updated_at"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        exclude = ["created_at", "updated_at"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at", "updated_at"]


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ["created_at", "updated_at"]


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        exclude = ["created_at", "updated_at"]
        extra_kwargs = {"service": {"required": False}}


class ServiceSerializer(serializers.ModelSerializer):
    # service_price = PriceSerializer(many=True, required=False)

    class Meta:
        model = Service
        exclude = ["created_at", "updated_at"]
        # extra_kwargs = {"service_price": {"required": True}}

    # def create(self, validated_data):
    #     service_prices = validated_data.pop("service_price", [])
    #     service_instance = Service.objects.create(**validated_data)
    #     for price in service_prices:
    #         Price.objects.create(service=service_instance, **price)
    #     return service_instance

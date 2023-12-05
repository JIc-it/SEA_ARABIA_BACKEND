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


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = [
            "thumbnail",
            "is_thumbnail",
        ]
        extra_kwargs = {"service": {"required": False}}


class ServiceSerializer(serializers.ModelSerializer):
    service_price = PriceSerializer(many=True)
    service_image = ServiceImageSerializer(many=True)
    destination = serializers.CharField(source="destination.name")
    company = serializers.CharField(source="company.name")
    category = serializers.CharField(source="category.name")
    pricing_type = serializers.CharField(source="pricing_type.name")
    occasions = serializers.SlugRelatedField(
        slug_field="name", queryset=Occasion.objects.all()
    )

    class Meta:
        model = Service
        exclude = ["created_at", "updated_at"]

        extra_kwargs = {
            "service_price": {"required": False},
            "service_image": {"required": False},
        }

    def create(self, validated_data):
        service_prices = validated_data.pop("service_price", [])
        service_images = validated_data.pop("service_image", [])
        ocassions = validated_data.pop("occasions", [])
        amenities = validated_data.pop("amenities", [])
        service_instance = Service.objects.create(**validated_data)
        service_instance.occasions.set(ocassions)
        service_instance.amenities.set(amenities)
        for price in service_prices:
            Price.objects.create(service=service_instance, **price)

        for service_image in service_images:
            ServiceImage.objects.create(service=service_instance, **service_image)
        return service_instance

    def update(self, instance, validated_data):
        service_prices = validated_data.pop("service_price", [])
        service_images = validated_data.pop("service_image", [])
        ocassions = validated_data.pop("occasions", [])
        amenities = validated_data.pop("amenities", [])
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        instance.occasions.set(ocassions)
        instance.amenities.set(amenities)

        return instance


class ExploreMoreSerializer(serializers.ModelSerializer):
    """serializer for showing the data in explore more section"""

    service_price = PriceSerializer(many=True)
    service_image = ServiceImageSerializer(many=True)
    destination = serializers.CharField(source="destination.name")
    company = serializers.CharField(source="company.name")
    category = serializers.CharField(source="category.name")
    # pricing_type = serializers.CharField(source="pricing_type.name")
    # occasions = serializers.SlugRelatedField(
    #     many=True, slug_field="name", queryset=Occasion.objects.all()
    # )
    amenities = AmenitySerializer(many=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "name",
            "pickup_point",
            "service_price",
            "capacity",
            "service_image",
            "destination",
            "company",
            "amenities",
            "description",
            "day",
            "night",
            "category",
        ]

        extra_kwargs = {
            "service_price": {"required": False},
            "service_image": {"required": False},
        }


class ServiceFilterList(serializers.ModelSerializer):
    """serializer for service review filter section"""

    service_image = ServiceImageSerializer(many=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "service_image",
        ]


class ServiceReviewSerializer(serializers.ModelSerializer):
    """serializer for creating new review"""

    class Meta:
        model = ServiceReview
        fields = [
            "service",
            "user",
            "review_title",
            "review_summary",
            "rating",
        ]


class ServiceReviewListSerializer(serializers.ModelSerializer):
    """service review listing"""

    service = serializers.CharField(source="service.name")
    user = serializers.CharField(source="user.first_name")

    class Meta:
        model = ServiceReview
        fields = [
            "service",
            "user",
            "review_title",
            "review_summary",
            "rating",
        ]

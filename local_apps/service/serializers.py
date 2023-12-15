from rest_framework import serializers
from .models import *
from local_apps.account.models import Bookmark
from local_apps.main.serializers import *


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ["id", "name"]


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name", "image"]


class ProfitMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitMethod
        fields = ["id", "name"]


class PriceCriterionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCriterion
        fields = ["id", "name"]


class DurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Duration
        fields = ["id", "time"]


class PriceListForPriceSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(required=False, allow_null=True)
    duration = DurationSerializer(required=False, allow_null=True)

    class Meta:
        model = PriceList
        fields = ['id',
                  'operation_type',
                  'destination',
                  'duration',
                  'price']


class PriceSerializer(serializers.ModelSerializer):
    profile_method = ProfitMethodSerializer(required=False, allow_null=True)
    price_criterion = PriceCriterionSerializer(required=False, allow_null=True)
    duration = DurationSerializer(required=False, allow_null=True)
    price_list = PriceListForPriceSerializer(required=False, allow_null=True)

    class Meta:
        model = Price
        fields = ['id',
                  'profile_method',
                  'price_criterion',
                  'price_per',
                  'price',
                  'sea_arabia_percentage',
                  'vendor_percentage',
                  'markup_fee',
                  'price_list',
                  'duration']


class PriceListSerializer(serializers.ModelSerializer):
    price_map = PriceSerializer(required=False, allow_null=True)
    destination = DestinationSerializer(required=False, allow_null=True)
    duration = DurationSerializer(required=False, allow_null=True)

    class Meta:
        model = PriceList
        fields = ['id',
                  'price_map',
                  'operation_type',
                  'destination',
                  'duration',
                  'price']


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id',
                  "thumbnail",
                  "is_thumbnail",
                  ]


class ServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id',
                  "name",
                  ]


class ServiceSerializer(serializers.ModelSerializer):
    price = PriceSerializer(required=False, allow_null=True)
    service_image = ServiceImageSerializer(
        many=True, required=False, allow_null=True)
    # company = ServiceCompanySerializer(required=False, allow_null=True)
    category = CategorySerializer(many=True, required=False, allow_null=True)
    sub_category = SubCategorySerializer(
        many=True, required=False, allow_null=True)
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['id',
                  'is_verified',
                  'is_active',
                  'is_top_suggestion',
                  'is_premium',
                  'is_bookmarked',
                  'type',
                  'category',
                  'sub_category',
                  'name',
                  'machine_id',
                  'description',
                  'lounge',
                  'bedroom',
                  'toilet',
                  'capacity',
                  'amenities',
                  'pickup_point',
                  'cancellation_policy',
                  'refund_policy',
                  'price',
                  'service_image',
                  'company',
                  'service_image',
                  ]

    def get_is_bookmarked(self, obj):
        try:
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                return Bookmark.objects.filter(user=request.user, service=obj).exists()
            return False
        except:
            return False


class ExploreMoreSerializer(serializers.ModelSerializer):
    """serializer for showing the data in explore more section"""

    price = PriceSerializer(required=False, allow_null=True)
    service_image = ServiceImageSerializer(many=True)
    destination = serializers.CharField(
        source="destination.name", required=False, allow_null=True)
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
            "price",
            "capacity",
            "service_image",
            "destination",
            "company",
            "amenities",
            "description",
            "category",
        ]

        extra_kwargs = {
            "service_price": {"required": False},
            "service_image": {"required": False},
        }


class ServiceFilterListSerializer(serializers.ModelSerializer):
    service_image = ServiceImageSerializer(
        many=True, required=False, allow_null=True)

    class Meta:
        model = Service
        fields = ["id", "name", "service_image",
                  "category", "sub_category", "company"]


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

    # def get_is_bookmarked(self, obj):
    #     request = self.context.get('request')
    #     user = request.user if request and request.user.is_authenticated else None
    #     if user:
    #         return Bookmark.objects.filter(user=user, service=obj).exists()
    #     return False

    # def to_representation(self, instance):
    #     data = super(ActivitySerializer, self).to_representation(instance)
    #     data['is_bookmarked'] = self.get_is_bookmarked(instance)
    #     return data


class ServiceAvailabilityServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id", "name"]


class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    service = ServiceAvailabilityServiceSerializer()

    class Meta:
        model = ServiceAvailability
        fields = ["id", "service", "date", "time", "created_at", "updated_at"]


class PackageSerializer(serializers.ModelSerializer):
    """for combopackeges"""
    class Meta:
        model = Package
        fields = ['id', 'service', 'name',
                  'short_description', 'capacity', 'image', 'price']

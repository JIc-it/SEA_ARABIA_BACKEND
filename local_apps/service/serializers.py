from rest_framework import serializers
from .models import *
from local_apps.account.models import Bookmark
from local_apps.main.serializers import *
from local_apps.booking.models import Booking
from import_export import resources, fields, widgets


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


class PriceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceType
        fields = ["id", "name","per_ticket",]


# class PriceCriterionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PriceCriterion
#         fields = ["id", "name"]


# class DurationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Duration
        # fields = ["id", "time"]


# class PriceListForPriceSerializer(serializers.ModelSerializer):
#     destination = DestinationSerializer(required=False, allow_null=True)
#     duration = DurationSerializer(required=False, allow_null=True)

#     class Meta:
#         model = PriceList
#         fields = ['id',
#                   'operation_type',
#                   'destination',
#                   'duration',
#                   'price']


class PriceSerializer(serializers.ModelSerializer):
    # profile_method = ProfitMethodSerializer(required=False, allow_null=True)
    # price_criterion = PriceCriterionSerializer(required=False, allow_null=True)
    # duration = DurationSerializer(required=False, allow_null=True)
    # price_list = PriceListForPriceSerializer(required=False, allow_null=True)
    location = serializers.CharField(source = "location.name")
    class Meta:
        model = Price
        fields = ['id',"service", "is_active", "name", "price", "is_range", "location",
            "duration_hour", "duration_minute", "duration_day","time",
            "end_time", "day", "end_day", "date", "end_date"
            ]


# class PriceListSerializer(serializers.ModelSerializer):
#     price_map = PriceSerializer(required=False, allow_null=True)
#     destination = DestinationSerializer(required=False, allow_null=True)
#     duration = DurationSerializer(required=False, allow_null=True)

#     class Meta:
#         model = PriceList
#         fields = ['id',
#                   'price_map',
#                   'operation_type',
#                   'destination',
#                   'duration',
#                   'price']


class ServiceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceImage
        fields = ['id',
                  "image",
                  "service"
                  ]


class ServiceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id',
                  "name",
                  ]


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ServiceSerializer(serializers.ModelSerializer):
    service_price_service = PriceSerializer(allow_null=True,many=True)
    service_image = ServiceImageSerializer(
        many=True, required=False, allow_null=True)
    # company = ServiceCompanySerializer(required=False, allow_null=True)
    category = CategorySerializer(many=True, required=False, allow_null=True)
    amenities = AmenitySerializer(many=True, required=False, allow_null=True)
    sub_category = SubCategorySerializer(
        many=True, required=False, allow_null=True)
    is_bookmarked = serializers.SerializerMethodField()
    company = serializers.CharField(source = "company.name")
    price_type = serializers.CharField(source = "price_type.name")
    profit_method = serializers.CharField(source = "profit_method.name")


    class Meta:
        model = Service
        fields = ['id',
                  'is_verified',
                  'is_active',
                  'is_top_suggestion',
                  'is_premium',
                  'is_bookmarked',
                  'is_sail_with_activity',
                #   'is_recommended',
                  'type',
                  'name',
                  'machine_id',
                  'description',
                  'lounge',
                  'bedroom',
                  'toilet',
                  'capacity',
                #   'pickup_point',
                  'cancellation_policy',
                  'refund_policy',
                  'service_image',
                  'company',
                  'category',
                  'amenities',
                  'sub_category',
                  'service_image',
                #   'price',
                  "is_duration",
                  "is_date",
                  "is_day",
                  "is_time",
                  "is_destination",
                  "price_type",
                  "profit_method",
                  "service_price_service",
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
    category = CategorySerializer(many=True, required=False, allow_null=True)
    amenities = AmenitySerializer(many=True, required=False, allow_null=True)

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
    """for combo package listing"""
    service = ServiceSerializer() 

    class Meta:
        model = Package
        fields = ['id', 'is_active', 'service', 'name', 'short_description', 'capacity', 'image', 'price']


class ServiceListSerializer(serializers.ModelSerializer):
    """ Serializer for listing the services """

    total_booking = serializers.SerializerMethodField(
        method_name="get_total_booking")
    company = serializers.CharField(source="company.name")
    category = serializers.StringRelatedField(many=True)
    sub_category = serializers.StringRelatedField(many=True)

    def get_total_booking(self, instance):
        try:
            total_count = Booking.objects.filter(service=instance).count()
            return total_count
        except:
            return 0

    class Meta:
        model = Service
        fields = [
            "id",
            "company",
            "category",
            "sub_category",
            "name",
            "status",
            "total_booking"
        ]


class ServiceListExportResource(resources.ModelResource):
    total_booking = fields.Field(
        column_name='total_booking', attribute='dehydrate_total_booking')
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=widgets.ManyToManyWidget(Category, field='name', separator=', ')
    )
    sub_category = fields.Field(
        column_name='sub_category',
        attribute='sub_category',
        widget=widgets.ManyToManyWidget(
            SubCategory, field='name', separator=', ')
    )
    is_active = resources.Field(column_name='status', attribute='is_active')

    def dehydrate_total_booking(self, instance):
        try:
            total_count = Booking.objects.filter(service=instance).count()
            return total_count
        except:
            return 0

    class Meta:
        model = Service
        fields = [
            "company__name",
            "category",
            "sub_category",
            "name",
            "is_active",
            "total_booking"
        ]

        export_order = fields

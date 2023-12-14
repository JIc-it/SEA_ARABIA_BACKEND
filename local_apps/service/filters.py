import django_filters
from .models import *


class SubCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = SubCategory
        fields = ["category"]


class ServiceFilter(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = [
            "is_verified",
            "is_active",
            "is_premium",
            "company",
            "category",
            "sub_category",
            "pickup_point",
            "amenities",
            "type",
        ]


class ServiceReviewFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceReview
        fields = [
            "rating",
        ]

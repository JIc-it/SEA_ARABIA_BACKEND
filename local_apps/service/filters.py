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
            "category",
            "company",
            "occasions",
            "pickup_point",
            "destination",
            "capacity",
            "amenities",
        ]

import django_filters
from .models import *


class SubCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = SubCategory
        fields = ["category"]





class ServiceFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method="get_category")
  

    def get_category(self, queryset, name, value):
        try:
            # Split the comma-separated values into a list
            categories = value.split(",")
            
            # Filter services based on multiple category names
            return queryset.filter(category__in=categories)
        except Exception as e:
            # Handle exceptions if needed
            return queryset.none()

    class Meta:
        model = Service
        fields = [
            "is_verified",
            "is_active",
            "is_premium",
            "is_sail_with_activity",
            "is_top_suggestion",
            "company",
            "category",
            "sub_category",
            "pickup_point",
            "amenities",
            "type",
        ]



# class ServiceFilter(django_filters.FilterSet):
#     class Meta:
#         model = Service
#         fields = [
#             "is_verified",
#             "is_active",
#             "is_premium",
#             "company",
#             "category",
#             "sub_category",
#             "pickup_point",
#             "amenities",
#             "type",
#         ]



# class ServiceFilter(django_filters.FilterSet):
#     class Meta:
#         model = Service
#         fields = [
#             "is_verified",
#             "is_active",
#             "is_premium",
#             "company",
#             "category",
#             "sub_category",
#             "pickup_point",
#             "amenities",
#             "type",
#         ]

#     def filter_queryset(self, queryset):
#         queryset = super().filter_queryset(queryset)

#         # Get the service_type from the request data
#         service_type = self.request.GET.get("type")

#         # If service_type is "activity," filter categories based on the service_type
#         if service_type == "activity":
#             queryset = queryset.filter(type="activity")

#             # Get distinct category names for activities
#             activity_categories = Category.objects.filter(service_service_category__type="activity").distinct()

#             # Filter the queryset to include only services with categories related to the activity
#             queryset = queryset.filter(category__in=activity_categories)

#         return queryset



class ServiceReviewFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceReview
        fields = [
            "rating",
        ]



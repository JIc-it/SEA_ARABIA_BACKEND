import django_filters
from .models import *
from django import forms


class VendorFilter(django_filters.FilterSet):
    """filter for filtering out the company status"""

    status = django_filters.CharFilter(
        field_name="company_company_user__status__name")

    class Meta:
        model = User
        fields = [
            "status",
        ]


class UserFilter(django_filters.FilterSet):
    """ filtering user based on the role type   """

    role = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(method="get_location")
    created_at = django_filters.CharFilter(method="get_created_at")
    company_company_user = django_filters.BooleanFilter(
        method='get_company_company_user')

    def get_location(self, queryset, name, value):
        """ function returns the result with multiple location selected """
        try:
            locations = value.split(",")
            return queryset.filter(profileextra__location__location__in=locations)
        except Exception as e:
            return queryset.none()

    def get_created_at(self, queryset, name, value):
        start_date, end_date = value.split(',')
        return queryset.filter(created_at__date__gte=start_date, created_at__date__lte=end_date)

    def get_company_company_user(self, queryset, name, value):
        if value:
            return queryset.filter(company_company_user__is_active=True)

    class Meta:
        model = User
        fields = [
            "role",
            "location",
            "created_at",
            "company_company_user"
        ]

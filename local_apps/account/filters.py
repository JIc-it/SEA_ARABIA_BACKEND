import django_filters
from .models import *
from django import forms 

class VendorFilter(django_filters.FilterSet):
    """filter for filtering out the company status"""

    status = django_filters.CharFilter(field_name="company_company_user__status__name")

    class Meta:
        model = User
        fields = [
            "status",
        ]



class UserFilter(django_filters.FilterSet):
    """ filtering user based on the role type   """

    role = django_filters.CharFilter(lookup_expr="icontains")
    location = django_filters.CharFilter(method = "get_location")
    updated_at = django_filters.DateFilter(method="get_updated_at")

    def get_location(self,queryset,name,value):
        """ function returns the result with multiple location selected """
        try:
            locations = value.split(",")
            return queryset.filter(profileextra__location__in = locations)
        except Exception as e:
            return queryset.none()
        
    def get_updated_at(self,queryset,name,value):
        print(value,name,'<<<<<')
        return queryset
        
    class Meta:
        model = User
        fields = [
            "role",
            "location",
            "updated_at"
        ]



import django_filters
from .models import *


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Company
        fields = [
            "is_onboard",
            "is_active",
            "assigned_to",
            "service_summary",
            "status",
        ]

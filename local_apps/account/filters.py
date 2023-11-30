import django_filters
from .models import *


class VendorFilter(django_filters.FilterSet):
    """filter for filtering out the company status"""

    status = django_filters.CharFilter(field_name="company_company_user__status")

    class Meta:
        model = User
        fields = [
            "status",
        ]

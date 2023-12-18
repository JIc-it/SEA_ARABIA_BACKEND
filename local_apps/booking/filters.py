import django_filters
from .models import *


class BookingFilter(django_filters.FilterSet):
    vendor = django_filters.UUIDFilter(field_name="service__company__user")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Booking
        fields = [
            "service",
            "vendor",
            "status",
        ]
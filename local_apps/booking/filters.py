import django_filters
from .models import *


class BookingFilter(django_filters.FilterSet):
    vendor = django_filters.UUIDFilter(field_name="service__company__user")

    class Meta:
        model = Booking
        fields = [
            "service",
            "vendor",
        ]

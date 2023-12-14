import django_filters
from .models import *


class BookingFilter(django_filters.FilterSet):
    class Meta:
        models = Booking
        fields = [
            "service"
            "service__company__user"
        ]

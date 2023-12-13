import django_filters
from .models import Offer


class OfferFilter(django_filters.FilterSet):
    class Meta:
        model = Offer
        fields = [
            'display_global',
        ]

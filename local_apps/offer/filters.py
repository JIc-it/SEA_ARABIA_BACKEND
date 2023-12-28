import django_filters
from .models import Offer


class OfferFilter(django_filters.FilterSet):
    expiry_start_date = django_filters.CharFilter(
        field_name='end_date',
        lookup_expr='gte',
    )

    expiry_end_date = django_filters.CharFilter(
        field_name='end_date',
        lookup_expr='lte',
    )

    class Meta:
        model = Offer
        fields = [
            'is_enable',
            'expiry_start_date',
            'expiry_end_date'
        ]

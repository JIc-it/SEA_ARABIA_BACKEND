import django_filters
from .models import *
from datetime import datetime

class DateFilter(django_filters.DateFilter):
    def filter(self, qs, value):
        if value:
            value = datetime.combine(value, datetime.min.time())  # Combine date with minimum time
            return super().filter(qs, value)
        return qs

class OfferFilter(django_filters.FilterSet):
    expiry_start_date = DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label='Expiry Start Date (greater than or equal to)'
    )

    expiry_end_date = DateFilter(
        field_name='end_date',
        lookup_expr='lte',
        label='Expiry End Date (less than or equal to)'
    )

    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Name contains'
    )

    is_enable = django_filters.Filter(
        field_name='is_enable',
        method='filter_is_enable'
    )

    def filter_is_enable(self, queryset, name, value):
        data_true = True if value in ['True', 'true', True] else None
        data_false = False if value in ['False', 'false', False] else None
        value = data_true if data_true else data_false
        return queryset.filter(**{name: value})

    class Meta:
        model = Offer
        fields = [
            'is_enable',
            'expiry_start_date',
            'expiry_end_date',
            'name',
        ]
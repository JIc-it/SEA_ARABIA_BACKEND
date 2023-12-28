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

    is_enable = django_filters.Filter(
        field_name='is_enable',
        method='filter_is_enable'
    )

    def filter_is_enable(self, queryset, name, value):
        data_true = True if value == 'True' or value == 'true' or value == True else None
        data_false = False if value == 'False' or value == 'false' or value == False else None
        value = data_true if data_true else data_false
        return queryset.filter(**{name: value})

    class Meta:
        model = Offer
        fields = [
            'is_enable',
            'expiry_start_date',
            'expiry_end_date'
        ]

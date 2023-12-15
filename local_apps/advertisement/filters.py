import django_filters
from .models import *

class AdvertisementFilter(django_filters.FilterSet):
    """ filtering the Advertisement based on the name """
    class Meta:
        model = Advertisement
        fields = ["name","is_active"]

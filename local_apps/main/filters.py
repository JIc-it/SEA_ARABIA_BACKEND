import django_filters
from .models import *


class SubcategoryFilter(django_filters.FilterSet):
    """ filtering the subcategory based on the category id """

    class Meta:
        model = SubCategory
        fields = ["category"]

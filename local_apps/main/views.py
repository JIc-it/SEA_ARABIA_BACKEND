from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SubcategoryFilter
from .models import *
from .serializers import *


# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page

# @method_decorator(cache_page(60 * 15), name='dispatch') 
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# @method_decorator(cache_page(60 * 15), name='dispatch')
class SubcategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SubcategoryFilter

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SubcategoryFilter
from .models import *
from .serializers import *

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryList(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = SubcategoryFilter
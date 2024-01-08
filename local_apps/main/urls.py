from django.urls import path
from .views import *

urlpatterns = [
    path('category-list', CategoryList.as_view(), name="category-list"),
    path('subcategory-list', SubcategoryList.as_view(), name="subcategory-list")
]

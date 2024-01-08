from django.urls import path
from .views import *

urlpatterns = [
    path('advertisement-create/', AdvertisementCreate.as_view(), name="advertisement-create"),
    path('advertisements/', AdvertisementList.as_view(), name="advertisements"),
]

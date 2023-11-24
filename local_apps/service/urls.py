from django.urls import path
from .views import *


urlpatterns = [
    # ocassion urls
    path(
        "occassion-list",
        OccassionList.as_view(),
        name="ocassion_list",
    ),
    # vendor price type urls
    path(
        "vendorprice-type-list",
        VendorPriceTypeList.as_view(),
        name="vendorprice_type_list",
    ),
    path(
        "vendorprice-type-create",
        VendorPriceTypeCreate.as_view(),
        name="vendorprice_type_create",
    ),
    path(
        "vendorprice-type-update/<uuid:pk>",
        VendorPriceTypeUpdate.as_view(),
        name="vendorprice_type_update",
    ),
    # Destination  urls
    path(
        "destination-list",
        DestinationList.as_view(),
        name="destination_list",
    ),
    path(
        "destination-create",
        DestinationCreate.as_view(),
        name="destination_create",
    ),
    path(
        "destination-update/<uuid:pk>",
        DestinationUpdate.as_view(),
        name="destination_update",
    ),
    # Amenity  urls
    path(
        "amenity-list",
        AmenityList.as_view(),
        name="amenity_list",
    ),
    # Category  urls
    path(
        "category-list",
        CategoryList.as_view(),
        name="category_list",
    ),
    # SubCategory  urls
    path(
        "subcategory-list",
        SubCategoryList.as_view(),
        name="subcategory_list",
    ),
    # Service  urls
    path(
        "service-list",
        ServiceList.as_view(),
        name="service_list",
    ),
    path(
        "service-create",
        ServiceCreate.as_view(),
        name="service_create",
    ),
    path(
        "service-view/<uuid:pk>",
        ServiceView.as_view(),
        name="service_view",
    ),
    path(
        "service-update/<uuid:pk>",
        ServiceUpdate.as_view(),
        name="service_update",
    ),
]

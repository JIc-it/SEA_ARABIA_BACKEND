from django.urls import path
from .views import *

urlpatterns = [
    # vendor price type urls
    # path(
    #     "vendorprice-type-list",
    #     VendorPriceTypeList.as_view(),
    #     name="vendorprice_type_list",
    # ),
    # path(
    #     "vendorprice-type-create",
    #     VendorPriceTypeCreate.as_view(),
    #     name="vendorprice_type_create",
    # ),
    # path(
    #     "vendorprice-type-update/<uuid:pk>",
    #     VendorPriceTypeUpdate.as_view(),
    #     name="vendorprice_type_update",
    # ),
    # Destination  urls
    path(
        "destination-list",
        DestinationList.as_view(),
        name="destination_list"
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
    #   Service Price urls
    path(
        "service-price-update/<uuid:pk>",
        ServicePriceUpdate.as_view(),
        name="service-price-update",
    ),
    #   Service Image urls

    path(
        "service-image-update/<uuid:pk>",
        ServiceImageUpdate.as_view(),
        name="service-image-update",
    ),
    path(
        "service-image/create",
        ServiceImageCreate.as_view(),
        name="service-image-create",
    ),
    path(
        "service-image/status/<uuid:pk>",
        ServiceImageStatus.as_view(),
        name="service-image-status"
    ),
    path(
        "service-image/delete/<uuid:pk>", ServiceImageDelete.as_view(), name="service-image-status"),

    #   Service Review Serializer
    path(
        "service-review-create",
        ServiceReviewCreate.as_view(),
        name="service-review-create",
    ),
    path(
        "service-review-list/<uuid:pk>",
        ServiceReviewList.as_view(),
        name="service-review-list",
    ),
    path(
        "service-filter-list",
        ServiceFilterList.as_view(),
        name="service-filter-list",
    ),
    #  App Urls
    path(
        "explore-more",
        ExploreMore.as_view(),
        name="explore-more",
    ),
    # top suggestions
    path(
        "top-suggestions",
        ServiceTopSuggestion.as_view(),
        name="top-suggestions",
    ),
    # review list
    path(
        "service-review-applist/<uuid:pk>",
        ServiceReviewListApp.as_view(),
        name="service-review-applist",
    ),
    # category based list
    path("category-based-listing/<str:category_name>/",
         CategoryBasedListing.as_view(),
         name="category-based-listing"
         ),

    path('servicesavailable/<str:date>/<uuid:service_id>/',
         ServiceAvailabeListView.as_view(), name='service-availabe'),
    # Combo package list
    path('combopackages', ComboPackageListing.as_view(), name='combopackages'),

    path('service-booking-availability/<uuid:service>/<str:date>/',
         AdminServiceBookingAvailabilityList.as_view(), name='service-booking-availability'),

    path('service-filter-list-cms',
         ServiceFilterAdminList.as_view(), name='service-filter-list-cms'),

    path('service_availablitytime_list/<str:date>/<uuid:pk>',
         ServiceAvailablityTime.as_view(), name='service_availablity_time_list'),

    path('service_availablitytime_update/<uuid:pk>',
         ServiceAvailablityTimeUpdate.as_view(), name='service_availablitytime_update'),

    # service listing for app side
    
    path('service-listapp',
         ServiceListApp.as_view(), name='service-listapp'),

    path('export-service-list', ExportServiceCSVView.as_view(),
         name='export-service-list'),

    # Package listing for cms side

    path('package-create',
         PackageCreateAPIView.as_view(), name='package-create'),
    
    path('package-update/<uuid:pk>',
         PackageUpdateAPIView.as_view(), name='package-update'),

    path('package-remove/<uuid:pk>',
         PackagDeleteAPIView.as_view(), name='package-remove'),

    path('package-list',
         PackageListAPIView.as_view(), name='package-list'),

    path('price-type-list',
         PriceTypeList.as_view(), name='price-type-list'),

    path('profit-method-list',
         ProfitMethodList.as_view(), name='profit-method-list'),
]


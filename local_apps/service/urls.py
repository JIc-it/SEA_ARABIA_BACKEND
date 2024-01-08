from django.urls import path
from .views import *

urlpatterns = [

    # Destination urls
    path("destination-list", DestinationList.as_view(), name="destination_list"),
    path("destination-create", DestinationCreate.as_view(), name="destination_create"),
    path("destination-update/<uuid:pk>", DestinationUpdate.as_view(), name="destination_update"),

    # Amenity urls
    path("amenity-list", AmenityList.as_view(), name="amenity_list"),

    # Category urls
    path("category-list", CategoryList.as_view(), name="category_list"),

    # SubCategory urls
    path("subcategory-list", SubCategoryList.as_view(), name="subcategory_list"),

    # Service urls
    path("service-list", ServiceList.as_view(), name="service_list"),
    path("service-create", ServiceCreate.as_view(), name="service_create"),
    path("service-view/<uuid:pk>", ServiceView.as_view(), name="service_view"),
    path("service-update/<uuid:pk>", ServiceUpdate.as_view(), name="service_update"),

    # Service Price urls
    path("service-price-update/<uuid:pk>", ServicePriceUpdate.as_view(), name="service-price-update"),

    # Service Image urls
    path("service-image-update/<uuid:pk>", ServiceImageUpdate.as_view(), name="service-image-update"),
    path("service-image/create", ServiceImageCreate.as_view(), name="service-image-create"),
    path("service-multiple-image/create", ServiceMultipleImageCreate.as_view(), name="service-multiple-image-create"),
    path("service-image/status/<uuid:pk>", ServiceImageStatus.as_view(), name="service-image-status"),
    path("service-image/delete/<uuid:pk>", ServiceImageDelete.as_view(), name="service-image-status"),

    # Service Review Serializer
    path("service-review-create", ServiceReviewCreate.as_view(), name="service-review-create"),
    path("service-review-list/<uuid:pk>", ServiceReviewList.as_view(), name="service-review-list"),
    path("service-filter-list", ServiceFilterList.as_view(), name="service-filter-list"),

    # App Urls
    path("explore-more", ExploreMore.as_view(), name="explore-more"),
    path("top-suggestions", ServiceTopSuggestion.as_view(), name="top-suggestions"),
    path("service-review-app-list/<uuid:pk>", ServiceReviewListApp.as_view(), name="service-review-app-list"),
    path("category-based-listing/<str:category_name>/", CategoryBasedListing.as_view(), name="category-based-listing"),
    path("service-available/<str:date_or_month>/<uuid:service_id>/", ServiceAvailabilityListView.as_view(),
         name="service-available"),

    # Combo package list
    path("combo-packages", ComboPackageListing.as_view(), name="combo-packages"),
    path("service-booking-availability/<uuid:service>/<str:month>/<str:date>/",
         AdminServiceBookingAvailabilityList.as_view(), name="service-booking-availability"),
    path("update-availability/<uuid:service>/<str:date>/", UpdateAvailabilityView.as_view(), name="mark-availability"),
    path("service-filter-list-cms", ServiceFilterAdminList.as_view(), name="service-filter-list-cms"),
    path("service_availability-time_list/<str:date>/<uuid:pk>", ServiceAvailablityTime.as_view(),
         name="service_availability_time_list"),
    path("service_availability-time_update/<uuid:pk>", ServiceAvailablityTimeUpdate.as_view(),
         name="service_availability-time_update"),

    # service availability create
    path("availability-create/", ServiceAvailabilityCreate.as_view(), name="availability-create"),

    # service availability retrieve
    path("availability-retrieve/<str:date>/<uuid:service>/", ServiceAvailabilityRetrieveView.as_view(),
         name="availability-retrieve"),

    # service listing for app side
    path("service-list-app", ServiceListApp.as_view(), name="service-list-app"),
    path("export-service-list", ExportServiceCSVView.as_view(), name="export-service-list"),

    # Package listing for cms side
    path("package-create", PackageCreateAPIView.as_view(), name="package-create"),
    path("package-update/<uuid:pk>", PackageUpdateAPIView.as_view(), name="package-update"),
    path("package-remove/<uuid:pk>", PackagDeleteAPIView.as_view(), name="package-remove"),
    path("package-list", PackageListAPIView.as_view(), name="package-list"),
    path("package-count", PackageCountsAPIView.as_view(), name="package-count"),
    path("package-view/<uuid:pk>", PackageView.as_view(), name="package-view"),
    path("price-type-list", PriceTypeList.as_view(), name="price-type-list"),
    path("profit-method-list", ProfitMethodList.as_view(), name="profit-method-list"),
    path("service/<uuid:pk>/", ServiceIndividualView.as_view(), name="service-detail"),
    path("price/delete/<uuid:pk>", ServicePriceDelete.as_view(), name="service-price-delete"),
    path("service-image/create", ServiceImageCreateMethod.as_view(), name="service-image-create"),
    path("admin/count", ServiceAdminCountView.as_view(), name="service_count_admin"),
]

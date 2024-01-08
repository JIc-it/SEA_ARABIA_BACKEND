from django.urls import path
from .views import *

urlpatterns = [
    # user urls
    path("google-auth", GoogleAuth.as_view(), name="google-auth"),
    path("user-create", UserCreate.as_view(), name="user-create"),
    path("user-list", UserList.as_view(), name="list-user"),
    path("user-update/<uuid:pk>", UserUpdate.as_view(), name="list-user"),

    # profile create urls
    path("user-profile-create", ProfileExtraCreate.as_view(), name="user-profile-create"),

    # Vendor urls
    # vendor list api
    path("vendor-list", VendorList.as_view(), name="vendor-list"),
    # vendor create api
    path("vendor-create", VendorAdd.as_view(), name="vendor-create"),
    # vendor Details api
    path("vendor-details/<uuid:pk>", VendorDetailsList.as_view(), name="vendor-details"),
    # vendor Details Add api
    path("vendor-add-details/<uuid:pk>", VendorDetailsAdd.as_view(), name="vendor-add-details"),
    # vendor personal Details list Add api
    path("vendor-list-details/<uuid:pk>", AllUserDetails.as_view(), name="vendor-list-details"),
    # vendor personal Details list Add api
    path("userid-type", UserIdTypeList.as_view(), name="userid-type"),

    # forget password urls
    path("check-first-time/", CheckFirstTimeLoginView.as_view(), name="check-first-time"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("profile-reset-password/", ProfileResetPasswordView.as_view(), name="profile-reset-password"),

    # admin Cms
    path("user-reset-password/", AllUserResetPasswordView.as_view(), name="all-user-reset-password"),

    # password reset url
    path("user-list/", UserListView.as_view(), name="user-list"),
    path("emilres/", emilres, name="emilres"),
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    

    # mobile app
    path('users-signup/', UserSignUp.as_view(), name='user-create'),
    path('users-profile/', UserProfileView.as_view(), name='user-profile'),
    path('users-update/<uuid:pk>', UserProfileUpdateView.as_view(), name='user-update'),

    # bookmark urls
    path('bookmark-create/', BookmarkCreateAPIView.as_view(), name="bookmark-create"),
    path('bookmark-list/', BookMarkListView.as_view(), name="bookmark-list"),
    path('bookmarks/delete/<uuid:service_id>/', BookMarkDeleteView.as_view(), name='bookmark-delete'),

    # vendor card count urls
    path('vendor-leads-count', VendorLeadCount.as_view(), name='vendor-leads-count'),

    # count of total users in cms
    path('user-count-admin', UserCountList.as_view(), name='user-count-admin'),
    # count of total users in cms
    path('vendor-count-admin', VendorCountList.as_view(), name='vendor-count-admin'),

    # guest user urls
    path("guest-user/list", GuestUserList.as_view(), name="guest_user_list"),

    # export
    path('vendor-list-export/', ExportVendorCSVView.as_view(), name='vendor-export-csv'),
    path('customer-list-export/', ExportCustomerCSVView.as_view(), name='customer-export-csv'),
    path('guests-list-export/', ExportGuestsCSVView.as_view(), name='guests-export-csv'),
    path('onboard-vendors-list-export/', ExportOnboardVendorsCSVView.as_view(), name='onboard-vendors-export-csv'),

    # gcc location listing
    path('gcc-locations', GCCLocationsAPIView.as_view(), name='gcc-locations'),
]

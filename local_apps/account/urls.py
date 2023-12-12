from django.urls import path
from .views import *

urlpatterns = [
    # user urls
    path(
        "user-create",
        UserCreate.as_view(),
        name="user-create",
    ),
    path(
        "user-list",
        UserList.as_view(),
        name="list-user",
    ),
    path(
        "user-update/<uuid:pk>",
        UserUpdate.as_view(),
        name="list-user",
    ),
    path(
        "user-delete/<uuid:pk>",
        UserDelete.as_view(),
        name="list-user",
    ),
    path(
        "user-view/<uuid:pk>",
        UserSerializerView.as_view(),
        name="user-view",
    ),
    # profilecreate urls
    path(
        "user-profile-create",
        ProfileExtraCreate.as_view(),
        name="user-profile-create",
    ),
    # Vendor urls
    # vendor list api
    path(
        "vendor-list",
        VendorSerializerList.as_view(),
        name="vendor-list",
    ),
    # vendor create api
    path(
        "vendor-create",
        VendorAdd.as_view(),
        name="vendor-create",
    ),
    # vendor Details api
    path(
        "vendor-details/<uuid:pk>",
        VendorDetailsList.as_view(),
        name="vendor-details",
    ),
    # vendor Details Add api
    path(
        "vendor-add-details/<uuid:pk>",
        VendorDetailsAdd.as_view(),
        name="vendor-add-details",
    ),
    # vendor personal Details list  Add api
    path(
        "vendor-list-details/<uuid:pk>",
        VendorPersonalList.as_view(),
        name="vendor-list-details",
    ),
    # vendor personal Details list  Add api
    path(
        "userid-type",
        UserIdTypeList.as_view(),
        name="userid-type",
    ),
    # forget password urls
    path(
        "check-first-time/", CheckFirstTimeLoginView.as_view(), name="check-first-time"
    ),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path(
        "profile-reset-password/",
        ProfileResetPasswordView.as_view(),
        name="profile-reset-password",
    ),


    path("user-list/", UserListView.as_view(), name="user-list"),
    path("emilres/", emilres, name="emilres"),
    path("request-otp/", RequestOTPView.as_view(), name="request-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("reset-passwordnew/",ForgotResetPasswordViewsnew.as_view(),name="reset-password-new",),

    #mobileapp
    
    path('users-signup/', UserSignUp.as_view(), name='user-create'),
    path('users-profile/', UserProfileView.as_view(), name='user-profile'),
    path('users-update/', UserProfileUpdateView.as_view(), name='user-update'),

    #bookmark urls

    path('bookmark-create/',BookMarkCreationAPI.as_view(),name="bookmark-create"),
    path('bookmark-list/',BookMarkListView.as_view(),name="bookmark-list"),
    path('bookmark-delete/<uuid:pk>/',BookMarkDeleteView.as_view(),name="bookmark-delete"),





    
]

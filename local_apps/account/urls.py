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
    # Vendor List urls
    path(
        "vendor-list",
        VendorSerializerList.as_view(),
        name="vendor-list",
    ),
]

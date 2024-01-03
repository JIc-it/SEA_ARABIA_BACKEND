from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from local_apps.account.views import LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('report/', include('local_apps.api_report.urls', namespace='report')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("company/", include("local_apps.company.urls")),
    path("service/", include("local_apps.service.urls")),
    path("account/", include("local_apps.account.urls")),
    path("booking/", include("local_apps.booking.urls")),
    path("offer/", include("local_apps.offer.urls")),
    path("main/", include("local_apps.main.urls")),
    path("advertisement/", include("local_apps.advertisement.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

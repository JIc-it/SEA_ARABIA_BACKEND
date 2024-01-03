from django.urls import path
from .views import *

app_name = "report"


urlpatterns = [
    path('log-list/', ActionLogListAPIView.as_view(), name='log-list'),
]
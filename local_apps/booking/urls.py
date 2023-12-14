from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingView.as_view(), name='booking-retrieve'),
    path('booking-count', BookingCardCount.as_view(), name='booking-count'),
    path('booking-statusupdate/<uuid:pk>', BookingStatusUpdate.as_view(),
         name='booking-statusupdate'),

]

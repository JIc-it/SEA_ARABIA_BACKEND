from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/admin/', AdminBookingListView.as_view(), name='booking-admin-list'),
    path('bookings/vendor/', VendorBookingListView.as_view(), name='booking-vendor-list'),
    path('bookings/user/', UserBookingListView.as_view(), name='booking-user-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingView.as_view(), name='booking-retrieve'),
    path('booking-count', BookingCardCount.as_view(), name='booking-count'),
    path('booking-status-update/<uuid:pk>', BookingStatusUpdate.as_view(), name='booking-status-update'),
    path('booking-export/', ExportBooking.as_view(), name='booking-export'),
    path('booking-cancellation/<uuid:pk>', BookingCancellation.as_view(), name='booking-cancellation'),

]

from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/admin/', AdminBookingListView.as_view(),
         name='booking-admin-list'),
    path('bookings/vendor/', VendorBookingListView.as_view(),
         name='booking-vendor-list'),
    path('bookings/user/', UserBookingListView.as_view(), name='booking-user-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingView.as_view(), name='booking-retrieve'),
    path('admin-booking-count/',
         AdminBookingCardCount.as_view(), name='booking-count'),
    path('booking-status-update/<uuid:pk>',
         BookingStatusUpdate.as_view(), name='booking-status-update'),
    path('admin-booking-count/',
         AdminBookingCardCount.as_view(), name='booking-count'),
    path('booking-status-update/<uuid:pk>',
         BookingStatusUpdate.as_view(), name='booking-status-update'),
    path('booking-export/', ExportBooking.as_view(), name='booking-export'),

     # Booking Cancellation In Admin CMS and Vendor CMS
    path('booking-cancellation/<uuid:pk>',
         BookingCancellation.as_view(), name='booking-cancellation'),

    path('vendor-booking-count/', VendorBookingCardCount.as_view(),
         name='booking-cancellation'),
         
    # Admin Individual Booking View For Admin CMS
    path('admin-booking-view/<uuid:pk>', AdminIndividualBookingView.as_view(),
         name='booking-view-admincms'),

     # Initialize Refund For Admin CMS
     path('initilize-refund-admin/<uuid:pk>', InitializeRefund.as_view(),
         name='initilize-refund-admincms'),
  
    path('payment-finalization', PaymentFinalization.as_view(),
         name='payment-finalization'),


]

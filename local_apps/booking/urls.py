from django.urls import path
from .views import *

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingView.as_view(), name='booking-retrieve'),
    path('booking-count', BookingCardCount.as_view(), name='booking-count'),
    path('booking-statusupdate/<uuid:pk>', BookingStatusUpdate.as_view(),
         name='booking-statusupdate'),
    path('bookings-applist', BookingAppList.as_view(), name='booking-applist'),
    path('booking-list-export/', ExportBookingCSVView.as_view(), name='booking-list-export'),
    path('booking-cancellation/<uuid:pk>', BookingCancellation.as_view(), name='booking-cancellation'),

    #Admin Cms All Booking List
    path('all-booking-list', AllBookingListView.as_view(), name='booking-List'),




]

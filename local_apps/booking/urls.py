# urls.py

from django.urls import path
from .views import OffersList, OffersDetail, BookingList, BookingDetail, PassengerDetailsList, PassengerDetailsDetail

urlpatterns = [
    path('offers/', OffersList.as_view(), name='offers-list'),
    path('offers/<int:pk>/', OffersDetail.as_view(), name='offers-detail'),
    path('bookings/', BookingList.as_view(), name='booking-create'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
    path('bookings/<int:booking_pk>/passengerdetails/', PassengerDetailsList.as_view(), name='passengerdetails-list'),
    path('bookings/<int:booking_pk>/passengerdetails/<int:pk>/', PassengerDetailsDetail.as_view(), name='passengerdetails-detail'),
]

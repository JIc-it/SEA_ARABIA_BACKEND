from django.urls import path
from .views import *

urlpatterns = [
    path('offers/admin', AdminOfferListView.as_view(), name='offer-list-admin'),
    path('offers/beastdeals', BeastDealsOfferListView.as_view(), name='offer-bestdeals'),
    path('offers/create/', OfferCreateView.as_view(), name='offer-create'),
    path('offers/<uuid:pk>/', OfferRetrieveView.as_view(), name='offer-retrieve'),
    path('offers/<uuid:pk>/update/', OfferUpdateView.as_view(), name='offer-update'),
]

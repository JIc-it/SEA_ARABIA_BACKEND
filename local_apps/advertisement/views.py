from django.shortcuts import render
from .models import*
from .serializers import*
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter
from random import shuffle
from django.db.models import F




# Create your views here.


class AdvertisementCreate(generics.CreateAPIView):
    """advertisement creation"""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter





class AdvertisementList(generics.ListAPIView):
    """advertisement random listing"""
    # Retrieve all advertisements and randomize their order
    queryset = Advertisement.objects.annotate(random_order=F('id')).order_by('?')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
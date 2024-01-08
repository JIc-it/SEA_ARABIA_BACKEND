from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework.response import Response
from utils.action_logs import create_log
from .models import*
from .serializers import*
from rest_framework import generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AdvertisementFilter
from random import shuffle
from django.db.models import F
# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import cache_page


class AdvertisementCreate(generics.CreateAPIView):
    """advertisement creation"""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def create(self, request, *args, **kwargs):
        try:
            # Serialize the data before the advertisement creation
            value_before = serialize('json', [Advertisement()])

            response = super().create(request, *args, **kwargs)

            # Get the created advertisement instance
            advertisement = Advertisement.objects.get(pk=response.data['id'])

            # Serialize the data after the advertisement creation
            value_after = serialize('json', [advertisement])

            # Log the advertisement creation action
            log_user = request.user if request.user else 'Unknown User'
            log_title = "{model} entry {action} by {user}".format(
                model="Advertisement",
                action='Created',
                user=log_user
            )

            create_log(
                user=request.user,
                model_name='Advertisement',
                action_value='Create',
                title=log_title,
                value_before=value_before,
                value_after=value_after
            )

            return response
        except Exception as e:
            return Response(f"Error: {str(e)}", status=status.HTTP_400_BAD_REQUEST)

# @method_decorator(cache_page(60 * 15), name='dispatch') 
class AdvertisementList(generics.ListAPIView):
    """advertisement random listing"""
    # Retrieve all advertisements and randomize their order
    queryset = Advertisement.objects.annotate(random_order=F('id')).order_by('?')
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

from rest_framework import serializers
from .models import *



class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id','is_active','name','image']
        

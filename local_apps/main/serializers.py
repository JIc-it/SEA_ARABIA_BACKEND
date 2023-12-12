from rest_framework import serializers
from .models import *
from local_apps.service.serializers import ActivitySerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name",'image']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ["created_at", "updated_at"]


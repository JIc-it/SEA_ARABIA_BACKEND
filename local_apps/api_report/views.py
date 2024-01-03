from django.shortcuts import render
from .models import ActionLog
from .serializers import ActionLogSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter


class ActionLogListAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['user__name',
                     'user__user_id',
                     'user__role',
                     'user__email',
                     'model_name',
                     'action'
                     ]

from django.shortcuts import render
from .models import ActionLog
from .serializers import ActionLogSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class ActionLogListAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer
    permission_classes = [IsAuthenticated]

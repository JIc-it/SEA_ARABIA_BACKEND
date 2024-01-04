from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from .models import ActionLog
from .serializers import ActionLogSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter
from local_apps.account.models import User


class ActionLogListAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = [
                     'user__account_id',
                     'user__role',
                     'user__email',
                     'model_name',
                     'action'
                     ]


class ActionLogVendorsAPIView(generics.ListAPIView):
    queryset = ActionLog.objects.all()
    serializer_class = ActionLogSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = [
        'user__account_id',
        'user__role',
        'user__email',
        'model_name',
        'action'
    ]

    def get_queryset(self):
        queryset = ActionLog.objects.all()

        if self.request.user.is_staff:
            user_id = self.kwargs.get('user_id')

            if user_id is not None:
                queryset = queryset.filter(user__id=user_id)

        return queryset

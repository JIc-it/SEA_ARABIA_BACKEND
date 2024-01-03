from django.contrib import admin
from .models import *


@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'url', 'method')
    list_filter = ['user', 'timestamp', 'method']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ModelUpdateLog)
class ModelUpdateLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'timestamp')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ActionLog)
class ActionLogAdmin(admin.ModelAdmin):
    pass

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

from django.contrib import admin
from .models import *


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "created_at", "updated_at"]
    filter = ["is_active,", "created_at", "updated_at"]
    search_fields = ["name"]

from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['name','created_at','updated_at']
    pass
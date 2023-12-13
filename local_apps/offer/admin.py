from .models import *
from django.contrib import admin


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass

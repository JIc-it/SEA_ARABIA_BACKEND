from django.contrib import admin
from .models import *


@admin.register(PriceList)
class PriceListAdmin(admin.ModelAdmin):
    pass


@admin.register(Duration)
class DurationAdmin(admin.ModelAdmin):
    pass


@admin.register(PriceCriterion)
class PriceCriterionAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfitMethod)
class ProfitMethodAdmin(admin.ModelAdmin):
    pass


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceAvailability)
class ServiceAvailabilityAdmin(admin.ModelAdmin):
    pass

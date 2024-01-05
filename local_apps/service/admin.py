from django.contrib import admin
from .models import *


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
    list_display = ["service_id","name","created_at","updated_at"]
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


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    pass

@admin.register(PriceType)
class PriceTypeAdmin(admin.ModelAdmin):
    pass
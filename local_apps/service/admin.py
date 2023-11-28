from django.contrib import admin
from .models import *


@admin.register(Occasion)
class OcassionAdmin(admin.ModelAdmin):
    pass


@admin.register(VendorPriceType)
class VendorPriceTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
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

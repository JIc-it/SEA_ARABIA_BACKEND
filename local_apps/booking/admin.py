# admin.py

from django.contrib import admin
from .models import Offers, Booking, PassengerDetails

@admin.register(Offers)
class OffersAdmin(admin.ModelAdmin):
    list_display = ('offername', 'created_at', 'updated_at')
    search_fields = ['offername']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'start_date', 'end_date', 'is_confirmed', 'created_at', 'updated_at')
    search_fields = ['booking_id', 'user__username', 'location']
    list_filter = ['is_confirmed', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'

    # If you want to display PassengerDetails inline with Booking in the admin
    class PassengerDetailsInline(admin.StackedInline):
        model = PassengerDetails
        extra = 1

    inlines = [PassengerDetailsInline]

@admin.register(PassengerDetails)
class PassengerDetailsAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'created_at', 'updated_at')
    search_fields = ['name', 'booking__booking_id']

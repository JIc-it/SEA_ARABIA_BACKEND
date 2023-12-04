from django.db import models
from django.conf import settings
import shortuuid
from local_apps.core.models import Main
from local_apps.service.models import Service

class Booking(Main):
    booking_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.CASCADE, related_name='booking_offer')
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.CASCADE, related_name='booking_service')
    date_booked = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    usertypes = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    starting_point = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    number_of_people = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    is_confirmed = models.BooleanField(default=False)
    is_insured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return self.booking_id

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = str('SA-BOK-' + shortuuid.ShortUUID().random(length=12))

        super(Booking, self).save(*args, **kwargs)



class PassengerDetials(Main):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, blank=True, null=True ,related_name='booking_passenger'
    )
    name = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "PassengerDetial"
        verbose_name_plural = "PassengerDetials"
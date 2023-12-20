from django.db import models
from django.conf import settings
from local_apps.core.models import Main
from local_apps.service.models import Service, Package
from local_apps.offer.models import Offer
from local_apps.account.models import Guest
BOOKING_STATUS = (
    ('Opened', 'Opened'),
    ('Successful', 'Successful'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

USER_TYPE = (
    ('Registered', 'Registered'),
    ('Guest', 'Guest'),
    ('Premium', 'Premium'),
)


BOOKING_CHOICE = (
    ("Booking", "Booking"),
    ("Enquiry", "Enquiry")
)


class Payment(Main):
    payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_id

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Booking(Main):
    booking_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='booking_booking_user')
    guest = models.ForeignKey(Guest,
                              on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='booking_booking_guest')
    offer = models.ForeignKey(Offer, blank=True, null=True,
                              on_delete=models.SET_NULL, related_name='booking_offer')
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='booking_service')
    payment = models.OneToOneField(Payment, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='booking_service')
    package = models.ForeignKey(Package, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='booking_booking_package')
    user_type = models.CharField(
        choices=USER_TYPE, default='Registered', max_length=255)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot = models.CharField(max_length=255, blank=True, null=True)
    additional_hours = models.PositiveIntegerField(default=0)
    additional_hours_amount = models.PositiveIntegerField(default=0)
    adults = models.PositiveIntegerField(default=0)
    children = models.PositiveIntegerField(default=0)
    is_insured = models.BooleanField(default=False)
    insurance_id = models.CharField(
        max_length=255, unique=True, blank=True, null=True)
    status = models.CharField(
        choices=BOOKING_STATUS, default='Opened', max_length=255, blank=True, null=True)
    booking_type = models.CharField(
        choices=BOOKING_CHOICE, default='Booking', max_length=255, blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return self.booking_id

from django.db import models
from django.conf import settings
from local_apps.core.models import Main
from local_apps.service.models import Service, Package, Price
from local_apps.offer.models import Offer
from local_apps.account.models import Guest

BOOKING_STATUS = (
    ('Upcoming', 'Upcoming'),
    ('Unsuccessful', 'Unsuccessful'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

REFUND_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
)

REFUND_TYPE = (
    ('Partial Amount', 'Partial Amount'),
    ('Full Amount', 'Full Amount'),
)

USER_TYPE = (
    ('Registered', 'Registered'),
    ('Guest', 'Guest'),
    ('Premium', 'Premium'),
)

BOOKING_FOR_TYPE = (
    ('My Self', 'My Self'),
    ('Someone Else', 'Someone Else'),
)

BOOKING_CHOICE = (
    ("Booking", "Booking"),
    ("Enquiry", "Enquiry")
)

BOOKING_ITEM_TYPE = (
    ("Service", "Service"),
    ("Activity", "Activity"),
    ("Package", "Package"),
    ("Event", "Event"),
)


class Payment(Main):
    payment_id = models.CharField(max_length=255)
    tap_pay_id = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    intial_response = models.JSONField(blank=True, null=True)
    confirmation_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.payment_id

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"


class Booking(Main):
    booking_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='booking_booking_user')
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='booking_booking_guest')
    offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='booking_booking_offer')
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='booking_booking_service')
    payment = models.OneToOneField(Payment, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='booking_booking_service')
    package = models.ForeignKey(Package, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='booking_booking_package')
    price = models.ForeignKey(Price, blank=True, null=True, on_delete=models.SET_NULL,
                              related_name='booking_booking_price')
    user_type = models.CharField(choices=USER_TYPE, default='Registered', max_length=255)
    booking_for = models.CharField(choices=BOOKING_FOR_TYPE, default='My Self', max_length=255)
    booking_item = models.CharField(choices=BOOKING_ITEM_TYPE, default='Service', max_length=255)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot_details = models.CharField(max_length=255, blank=True, null=True)
    additional_hours = models.PositiveIntegerField(default=0)
    additional_hours_amount = models.PositiveIntegerField(default=0)
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=BOOKING_STATUS, default='Opened', max_length=255, blank=True, null=True)
    booking_type = models.CharField(choices=BOOKING_CHOICE, default='Booking', max_length=255, blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    refund_status = models.CharField(choices=REFUND_STATUS, default=None, max_length=255, blank=True, null=True)
    refund_type = models.CharField(choices=REFUND_TYPE, default=None, max_length=255, blank=True, null=True)
    refund_amount = models.PositiveIntegerField(blank=True, null=True)
    refund_details = models.TextField(blank=True, null=True)
    price_total = models.PositiveIntegerField(default=0)
    user_details = models.JSONField(blank=True, null=True)
    guest_details = models.JSONField(blank=True, null=True)
    service_details = models.JSONField(blank=True, null=True)
    price_details = models.JSONField(blank=True, null=True)
    package_details = models.JSONField(blank=True, null=True)
    offer_details = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return self.booking_id 
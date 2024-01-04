from datetime import date

from django.core.serializers import serialize
from django.db import models
from django.conf import settings
from django.utils import timezone

from local_apps.api_report.middleware import get_current_request
from local_apps.api_report.models import ModelUpdateLog
from local_apps.core.models import Main
from local_apps.service.models import Service, Package, Price
from local_apps.offer.models import Offer
from local_apps.account.models import Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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
    initial_response = models.JSONField(blank=True, null=True)
    confirmation_response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.payment_id

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Payment.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Payment, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Payment, self).save(*args, **kwargs)

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
    user_type = models.CharField(
        choices=USER_TYPE, default='Registered', max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    booking_for = models.CharField(
        choices=BOOKING_FOR_TYPE, default='My Self', max_length=255)
    booking_item = models.CharField(
        choices=BOOKING_ITEM_TYPE, default='Service', max_length=255)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    selected_slots=models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot_details = models.CharField(max_length=255, blank=True, null=True)
    additional_hours = models.PositiveIntegerField(default=0)
    additional_hours_amount = models.PositiveIntegerField(default=0)
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(
        choices=BOOKING_STATUS, default='Opened', max_length=255, blank=True, null=True)
    booking_type = models.CharField(
        choices=BOOKING_CHOICE, default='Booking', max_length=255, blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    canceld_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='booking_canceld_user')
    refund_status = models.CharField(
        choices=REFUND_STATUS, default=None, max_length=255, blank=True, null=True)
    refund_type = models.CharField(
        choices=REFUND_TYPE, default=None, max_length=255, blank=True, null=True)
    refund_amount = models.PositiveIntegerField(blank=True, null=True)
    refund_details = models.TextField(blank=True, null=True)
    price_total = models.PositiveIntegerField(default=0)
    user_details = models.JSONField(blank=True, null=True)
    guest_details = models.JSONField(blank=True, null=True)
    service_details = models.JSONField(blank=True, null=True)
    price_details = models.JSONField(blank=True, null=True)
    package_details = models.JSONField(blank=True, null=True)
    offer_details = models.JSONField(blank=True, null=True)

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Booking.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Booking, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Booking, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return self.booking_id

    def save(self, *args, **kwargs):
        if not self.offer:
            super(Booking, self).save(*args, **kwargs)
            return
        temp_price = self.price.price if self.price and self.price.price else 0
        offer_amount = 0

        if self.booking_item in ['Activity', 'Service']:
            redeem_temp = False
            if self.offer.redemption_type in ['One-Time', 'Limited-Number']:
                if self.offer.redemption_type == 'One-Time' and self.offer.redeem_count < 1:
                    redeem_temp = True
                elif self.offer.redemption_type == 'Limited-Number' and self.offer.specify_no >= self.offer.redeem_count:
                    redeem_temp = True
            else:
                redeem_temp = True
            if self.price and self.offer and redeem_temp:
                if self.offer.discount_type == 'Percentage':
                    offer_amount = (temp_price * self.offer.discount_value) / 100
                    if offer_amount >= self.offer.up_to_amount:
                        offer_amount = self.offer.up_to_amount
                else:
                    offer_amount = self.offer.discount_value
                if self.offer.purchase_requirement and self.offer.min_purchase_amount <= temp_price:
                    self.price_total = temp_price - offer_amount
                else:
                    self.price_total = temp_price
            else:
                self.price_total = self.price if self.price and self.price.price else 0

            if self.offer.allow_multiple_redeem in ['One-Time', 'Multiple-Time']:
                if self.offer.allow_multiple_redeem == 'One-Time' and self.offer.multiple_redeem_count < 1:
                    redeem_temp = True
                elif self.offer.allow_multiple_redeem == 'Multiple-Time' and self.offer.multiple_redeem_specify_no >= self.offer.multiple_redeem_count:
                    redeem_temp = True
                else:
                    redeem_temp = True
                    if not redeem_temp:
                        raise ValidationError('You have already redeemed this Offer')
            if self.offer.expiration in ['No-Expiry', 'Limited-Time']:
                if self.offer.expiration == 'No-Expiry' and self.offer.start_date:
                    redeem_temp = True
                elif self.offer.expiration == 'Limited-Time' and self.offer.end_date:
                    if self.offer.end_date >= date.today():
                        redeem_temp = True
                else:
                    raise ValidationError("This Offer has expired")
            else:
                raise ValidationError("Invalid offer expiration")   
            if self.service in self.offer.services.all():
                redeem_temp=True
            else:
                raise ValidationError("The service provided does not match the service of this Offer.")

            if self.offer.purchase_requirement == True and self.price.price >= self.offer.min_purchase_amount:
                redeem_temp=True
                
            else: 
                redeem_temp= False

    #     elif self.booking_item in ['Package', 'Event']:
    #         self.price_total = self.package.price if self.package and self.package.price else 0
    #     else:
    #         self.price_total = 0

        if self.offer:
            self.offer.redeem_count = self.offer.redeem_count + 1

            self.offer.save()

        super(Booking, self).save(*args, **kwargs)


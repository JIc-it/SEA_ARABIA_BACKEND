from datetime import date
from django.db import models
from django.conf import settings
from local_apps.core.models import Main
from local_apps.service.models import Service, Package, Price
from local_apps.offer.models import Offer
from local_apps.account.models import Guest
from django.core.exceptions import ValidationError
from utils.id_handle import increment_two_digits, increment_two_letters, increment_one_letter

BOOKING_STATUS = (
    ('Opened', 'Opened'),
    ('Upcoming', 'Upcoming'),
    ('Unsuccessful', 'Unsuccessful'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

REFUND_STATUS = (
    (None, 'Default'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
)

REFUND_TYPE = (
    (None, 'Default'),
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
    prefix = models.CharField(max_length=10, default="SA-PMT")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=255)
    tap_pay_id = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)
    response = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.payment_id

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def generate_id_number(self):
        last_entry = Payment.objects.order_by('-created_at').first()
        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(last_entry.last_one_letter)
            else:
                self.last_one_letter = last_entry.last_one_letter

            if last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(last_entry.first_two_numbers)
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z',
                                                                                     'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(last_entry.last_two_numbers)

            self.payment_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.payment_id = f"{self.prefix}-AA00A00"

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.generate_id_number()
        super(Payment, self).save(*args, **kwargs)


class Booking(Main):
    prefix = models.CharField(max_length=10, default="SA-BKG-")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
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
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    booking_for = models.CharField(choices=BOOKING_FOR_TYPE, default='My Self', max_length=255)
    booking_item = models.CharField(choices=BOOKING_ITEM_TYPE, default='Service', max_length=255)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    slot_details = models.CharField(max_length=255, blank=True, null=True)
    additional_hours = models.PositiveIntegerField(default=0)
    additional_hours_amount = models.PositiveIntegerField(default=0)
    number_of_people = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=BOOKING_STATUS, default='Opened', max_length=255, blank=True, null=True)
    booking_type = models.CharField(choices=BOOKING_CHOICE, default='Booking', max_length=255, blank=True, null=True)
    cancellation_reason = models.TextField(blank=True, null=True)
    refund_status = models.CharField(choices=REFUND_STATUS, default='Default', max_length=255, blank=True, null=True)
    refund_type = models.CharField(choices=REFUND_TYPE, default='Default', max_length=255, blank=True, null=True)
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

    def generate_id_number(self):
        last_entry = Booking.objects.order_by('-created_at').first()
        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(last_entry.last_one_letter)
            else:
                self.last_one_letter = last_entry.last_one_letter

            if last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(last_entry.first_two_numbers)
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z', 'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(last_entry.last_two_numbers)

            self.booking_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.booking_id = f"{self.prefix}-AA00A00"

    def save(self, *args, **kwargs):
        try:
            # Automating booking_item
            if self.service and self.service.type:
                self.booking_item = self.service.type

            # if self.package and self.package.type:
            #     self.booking_item = self.service.type

            # Automating user_type
            if self.user:
                self.user_type = 'Registered'
            elif self.guest:
                self.user_type = 'Guest'
            else:
                self.user_type = None

            # Automating booking_type
            if self.service:
                self.booking_type = 'Booking'
            elif self.package:
                self.booking_type = 'Enquiry'
            else:
                self.booking_type = None

            # Generating booking_id
            if not self.booking_id:
                self.generate_id_number()

            # Checking if offer addition possible
            if self.service and self.offer and self.booking_item in ['Activity', 'Service']:

                # Raising validation error if offer not started or expired
                if self.offer.expiration in ['No-Expiry', 'Limited-Time']:
                    if self.offer.start_date and self.offer.start_date >= date.today():
                        raise ValidationError("Offer not started yet")
                    if self.offer.expiration == 'Limited-Time' and self.offer.end_date and self.offer.end_date <= date.today():
                        raise ValidationError("Offer has expired")
                else:
                    raise ValidationError("Invalid offer expiration")

                # Checking redeem count not exceeded
                redeem_temp = False
                if self.offer.redemption_type in ['One-Time', 'Limited-Number']:
                    if self.offer.redemption_type == 'One-Time' and self.offer.redeem_count >= 1:
                        raise ValidationError("Discount / Offer Redeem count exceeded...")
                    elif self.offer.redemption_type == 'Limited-Number' and self.offer.specify_no <= self.offer.redeem_count:
                        raise ValidationError("Discount / Offer Redeem count exceeded...")
                else:
                    raise ValidationError("Invalid redemption type")

                # Getting the user redeemed count of same service
                user_redeem_count = Booking.objects.filter(user=self.user, service=self.service,
                                                           offer=self.offer).count() if Booking.objects.filter(
                    user=self.user, service=self.service, offer=self.offer).exists() else 0

                # Allow multiple or single redeem on single service
                if self.offer.allow_multiple_redeem in ['One-Time', 'Multiple-Time']:
                    if self.offer.allow_multiple_redeem == 'One-Time' and user_redeem_count <= 1:
                        raise ValidationError('Offer already redeemed')
                    elif self.offer.allow_multiple_redeem == 'Multiple-Time' and self.offer.multiple_redeem_specify_no <= user_redeem_count:
                        raise ValidationError('Offer redeemed exceeded')
                else:
                    raise ValidationError("Invalid allow multiple redeem")

                if self.service not in self.offer.services.all():
                    raise ValidationError("Offer not available. Pleases try another one.")

                # Storing the current price on temp
                temp_price = self.price.price if self.price and self.price.price else 0

                # Storing the offer amount on temp
                offer_amount = 0

                # Calculating the offer amount
                if self.offer.discount_type == 'Percentage':
                    offer_amount = (temp_price * self.offer.discount_value) / 100
                    if offer_amount >= self.offer.up_to_amount:
                        offer_amount = self.offer.up_to_amount
                else:
                    offer_amount = self.offer.discount_value

                # Checking min purchase amount
                if self.offer.purchase_requirement and self.offer.min_purchase_amount <= temp_price:
                    self.price_total = temp_price - offer_amount
                else:
                    self.price_total = temp_price

                if self.offer:
                    self.offer.redeem_count = self.offer.redeem_count + 1
                    self.offer.save()

            super(Booking, self).save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(str(e))

from datetime import date
from django.db import models
from django.conf import settings
from local_apps.core.models import Main
from local_apps.service.models import Service, Package, Price
from local_apps.offer.models import Offer
from local_apps.account.models import Guest
from django.core.serializers import serialize
from django.core.exceptions import ValidationError
from utils.id_handle import increment_two_digits, increment_two_letters, increment_one_letter


class Payment(Main):
    # ID handling section
    prefix = models.CharField(max_length=10, default="SA-PMT")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    # Payment details
    tap_pay_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    initial_response = models.JSONField(blank=True, null=True)
    confirmation_response = models.JSONField(blank=True, null=True)

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
    BOOKING_STATUS = (
        (None, 'Default'),
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
        (None, 'Default'),
        ('Registered', 'Registered'),
        ('Guest', 'Guest'),
        ('Premium', 'Premium'),
    )

    BOOKING_FOR_TYPE = (
        (None, 'Default'),
        ('My Self', 'My Self'),
        ('Someone Else', 'Someone Else'),
    )

    BOOKING_CHOICE = (
        (None, 'Default'),
        ("Booking", "Booking"),
        ("Enquiry", "Enquiry")
    )

    BOOKING_ITEM_TYPE = (
        (None, 'Default'),
        ("Service", "Service"),
        ("Activity", "Activity"),
        ("Package", "Package"),
        ("Event", "Event"),
    )
    # ID handling section
    prefix = models.CharField(max_length=10, default="SA-BKG-")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    booking_id = models.CharField(max_length=255, unique=True, blank=True, null=True)

    # Mapping actual data
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

    # User / customer info
    user_type = models.CharField(choices=USER_TYPE, default='Default', max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)

    # Booking info
    destination = models.CharField(max_length=255, blank=True, null=True)
    booking_for = models.CharField(choices=BOOKING_FOR_TYPE, default='Default', max_length=255, blank=True, null=True)
    booking_item = models.CharField(choices=BOOKING_ITEM_TYPE, default='Default', max_length=255, blank=True, null=True)
    starting_point = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    slot_details = models.CharField(max_length=255, blank=True, null=True)
    additional_hours = models.PositiveIntegerField(default=0, blank=True, null=True)
    additional_hours_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    number_of_people = models.PositiveIntegerField(default=1, blank=True, null=True)
    booking_type = models.CharField(choices=BOOKING_CHOICE, default='Default', max_length=255, blank=True, null=True)
    status = models.CharField(choices=BOOKING_STATUS, default='Default', max_length=255, blank=True, null=True)

    # Cancellation & refund
    cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.JSONField(null=True, blank=True)
    refund_status = models.CharField(choices=REFUND_STATUS, default='Default', max_length=255, blank=True, null=True)
    refund_type = models.CharField(choices=REFUND_TYPE, default='Default', max_length=255, blank=True, null=True)
    refund_amount = models.PositiveIntegerField(blank=True, null=True)
    refund_details = models.TextField(blank=True, null=True)

    # Actual price
    price_total = models.PositiveIntegerField(default=0, blank=True, null=True)

    # Mapping data hard storing
    user_details = models.JSONField(blank=True, null=True)
    guest_details = models.JSONField(blank=True, null=True)
    service_details = models.JSONField(blank=True, null=True)
    price_details = models.JSONField(blank=True, null=True)
    package_details = models.JSONField(blank=True, null=True)
    offer_details = models.JSONField(blank=True, null=True)
    payment_details = models.JSONField(blank=True, null=True)

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

            if last_entry.first_two_numbers == 99 and last_entry.last_one_letter in ['Z',
                                                                                     'z'] and last_entry.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(last_entry.last_two_numbers)

            self.booking_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.booking_id = f"{self.prefix}-AA00A00"

    def save(self, *args, **kwargs):
        try:
            # Hard storing mapping datas
            if not self.user_details and self.user:
                self.user_details = serialize('json', [self.user])
            if not self.guest_details and self.guest:
                self.guest_details = serialize('json', [self.guest])
            if not self.offer_details and self.offer:
                self.offer_details = serialize('json', [self.offer])
            if not self.service_details and self.service:
                self.service_details = serialize('json', [self.service])
            if not self.payment_details and self.payment:
                self.payment_details = serialize('json', [self.payment])
            if not self.package_details and self.package:
                self.package_details = serialize('json', [self.package])
            if not self.price_details and self.price:
                self.price_details = serialize('json', [self.price])

            # Automating booking_item
            if self.service and self.service.type:
                self.booking_item = self.service.type

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

            # Checking if offer addition is possible
            if self.service and self.offer and self.booking_item in ['Activity', 'Service']:
                redeem_temp = False

                # Raising validation error if offer not started or expired
                if self.offer.expiration in ['No-Expiry', 'Limited-Time']:
                    if self.offer.start_date and self.offer.start_date >= date.today():
                        raise ValidationError("Offer not started yet")
                    if self.offer.expiration == 'Limited-Time' and self.offer.end_date and self.offer.end_date <= date.today():
                        raise ValidationError("Offer has expired")
                else:
                    raise ValidationError("Invalid offer expiration")

                # Checking redeem count not exceeded
                if self.offer.redemption_type in ['One-Time', 'Limited-Number']:
                    if self.offer.redemption_type == 'One-Time' and self.offer.redeem_count >= 1:
                        raise ValidationError("Discount/Offer Redeem count exceeded...")
                    elif self.offer.redemption_type == 'Limited-Number' and self.offer.specify_no <= self.offer.redeem_count:
                        raise ValidationError("Discount/Offer Redeem count exceeded...")
                else:
                    raise ValidationError("Invalid redemption type")

                # Getting the user redeemed count of the same service
                user_redeem_count = Booking.objects.filter(user=self.user, service=self.service,
                                                           offer=self.offer).count() if Booking.objects.filter(
                    user=self.user, service=self.service, offer=self.offer).exists() else 0

                # Allow multiple or single redeem on a single service
                if self.offer.allow_multiple_redeem in ['One-Time', 'Multiple-Time']:
                    if self.offer.allow_multiple_redeem == 'One-Time' and user_redeem_count <= 1:
                        raise ValidationError('Offer already redeemed')
                    elif self.offer.allow_multiple_redeem == 'Multiple-Time' and self.offer.multiple_redeem_specify_no <= user_redeem_count:
                        raise ValidationError('Offer redeemed exceeded')
                else:
                    raise ValidationError("Invalid allow multiple redeem")

                if self.service not in self.offer.services.all():
                    raise ValidationError("Offer not available. Please try another one.")

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

            elif not self.offer:  # Handle the case when self.offer is None
                self.price_total = temp_price

            # Additional conditions for offer expiration, multiple redeem, and service check
            if self.offer:
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
                if self.service in self.offer.services.all():
                    redeem_temp = True
                else:
                    raise ValidationError("The service provided does not match the service of this Offer.")
                if self.offer.purchase_requirement == True and self.price.price >= self.offer.min_purchase_amount:
                    redeem_temp = True
                else:
                    redeem_temp = False

            elif self.booking_item in ['Package', 'Event']:
                self.price_total = self.package.price if self.package and self.package.price else 0
            else:
                self.price_total = 0

            if self.offer:
                self.offer.redeem_count = self.offer.redeem_count + 1
                self.offer.save()

            super(Booking, self).save(*args, **kwargs)
        except Exception as e:
            raise ValidationError(str(e))
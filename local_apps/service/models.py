from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import models
from django.utils import timezone

from local_apps.api_report.middleware import get_current_request
from local_apps.api_report.models import ModelUpdateLog
from local_apps.company.models import Company
from local_apps.core.models import Main
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from local_apps.main.models import Category, SubCategory
from utils.file_handle import remove_file
from utils.id_handle import increment_one_letter, increment_two_digits, increment_two_letters


def default_false_time_slot():
    return [
        {'time': 0, 'make_slot_available': False},
        {'time': 1, 'make_slot_available': False},
        {'time': 2, 'make_slot_available': False},
        {'time': 3, 'make_slot_available': False},
        {'time': 4, 'make_slot_available': False},
        {'time': 5, 'make_slot_available': False},
        {'time': 6, 'make_slot_available': False},
        {'time': 7, 'make_slot_available': False},
        {'time': 8, 'make_slot_available': False},
        {'time': 9, 'make_slot_available': False},
        {'time': 10, 'make_slot_available': False},
        {'time': 11, 'make_slot_available': False},
        {'time': 12, 'make_slot_available': False},
        {'time': 13, 'make_slot_available': False},
        {'time': 14, 'make_slot_available': False},
        {'time': 15, 'make_slot_available': False},
        {'time': 16, 'make_slot_available': False},
        {'time': 17, 'make_slot_available': False},
        {'time': 18, 'make_slot_available': False},
        {'time': 19, 'make_slot_available': False},
        {'time': 20, 'make_slot_available': False},
        {'time': 21, 'make_slot_available': False},
        {'time': 22, 'make_slot_available': False},
        {'time': 23, 'make_slot_available': False},
    ]


def default_true_time_slot():
    return [
        {'time': 0, 'make_slot_available': True},
        {'time': 1, 'make_slot_available': True},
        {'time': 2, 'make_slot_available': True},
        {'time': 3, 'make_slot_available': True},
        {'time': 4, 'make_slot_available': True},
        {'time': 5, 'make_slot_available': True},
        {'time': 6, 'make_slot_available': True},
        {'time': 7, 'make_slot_available': True},
        {'time': 8, 'make_slot_available': True},
        {'time': 9, 'make_slot_available': True},
        {'time': 10, 'make_slot_available': True},
        {'time': 11, 'make_slot_available': True},
        {'time': 12, 'make_slot_available': True},
        {'time': 13, 'make_slot_available': True},
        {'time': 14, 'make_slot_available': True},
        {'time': 15, 'make_slot_available': True},
        {'time': 16, 'make_slot_available': True},
        {'time': 17, 'make_slot_available': True},
        {'time': 18, 'make_slot_available': True},
        {'time': 19, 'make_slot_available': True},
        {'time': 20, 'make_slot_available': True},
        {'time': 21, 'make_slot_available': True},
        {'time': 22, 'make_slot_available': True},
        {'time': 23, 'make_slot_available': True},
    ]


DAY_CHOICE = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)

TIME_CHOICES = [(str(time), str(time)) for time in range(0, 25)]
DURATION_HOUR_CHOICES = [(str(hour), str(hour)) for hour in range(0, 25)]
DURATION_MINUTE_CHOICES = [(str(minute), str(minute))
                           for minute in range(0, 61)]
DURATION_DAY_CHOICES = [(str(day), str(day)) for day in range(0, 32)]
DATE_CHOICES = [(str(date), str(date)) for date in range(32)]
DAY_CHOICES = [(i, str(i)) for i in range(1, 30)]

SERVICE_TYPE = (
    ("Service", "Service"),
    ("Activity", "Activity"),
)


class Destination(Main):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Destination.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Destination, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Destination, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"


class ProfitMethod(Main):
    name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [ProfitMethod.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(ProfitMethod, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(ProfitMethod, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Profit Method"
        verbose_name_plural = "Profit Methods"


class PriceType(Main):
    name = models.CharField(max_length=255, blank=True, null=True)
    per_ticket = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [PriceType.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(PriceType, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(PriceType, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Price type'
        verbose_name_plural = 'Price Types'


class Amenity(Main):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to="service/amenity/image")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Amenity.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Amenity, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Amenity, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = Amenity.objects.get(id=self.id)
            old_image = this_instance.image
        except Amenity.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(Amenity, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        self.create_update_log(data_before, None)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"


class Service(Main):
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_top_suggestion = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_sail_with_activity = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(
        choices=SERVICE_TYPE, max_length=100, default="Service", blank=True, null=True)
    category = models.ManyToManyField(
        Category, blank=True, related_name='service_service_category')
    sub_category = models.ManyToManyField(
        SubCategory, blank=True, related_name='service_service_sub_category')
    name = models.CharField(max_length=200, blank=True, null=True)
    machine_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lounge = models.PositiveIntegerField(blank=True, null=True)
    bedroom = models.PositiveIntegerField(blank=True, null=True)
    toilet = models.PositiveIntegerField(blank=True, null=True)
    capacity = models.CharField(max_length=200, blank=True, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    pickup_point_or_location = models.TextField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    refund_policy = models.TextField(blank=True, null=True)
    is_duration = models.BooleanField(default=False)
    is_date = models.BooleanField(default=False)
    is_day = models.BooleanField(default=False)
    is_time = models.BooleanField(default=False)
    is_destination = models.BooleanField(default=False)
    profit_method = models.ForeignKey(ProfitMethod, on_delete=models.SET_NULL, blank=True, null=True,
                                      related_name='service_service_profit_method')
    price_type = models.ForeignKey(PriceType, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='service_service_price_type')
    vendor_percentage = models.CharField(max_length=255, blank=True, null=True)
    sea_arabia_percentage = models.CharField(
        max_length=255, blank=True, null=True)
    markup_fee = models.PositiveIntegerField(blank=True, null=True)
    per_head_booking = models.BooleanField(default=False)
    purchase_limit_min = models.PositiveIntegerField(null=True, blank=True)
    purchase_limit_max = models.PositiveIntegerField(null=True, blank=True)
    # ID handling section
    prefix = models.CharField(max_length=10, default="SA-SER")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    service_id = models.CharField(max_length=255, blank=True, null=True)
    is_refundable = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.service_id if self.service_id else "No Service ID"

    def generate_id_number(self):
        last_entry = Service.objects.order_by('-created_at').first()
        if last_entry:
            self.last_two_numbers = last_entry.last_two_numbers + 1
            if self.last_two_numbers == 100:
                self.last_two_numbers = 0
                self.last_one_letter = increment_one_letter(last_entry.last_one_letter)

                if self.last_one_letter in ['Z', 'z']:
                    self.first_two_numbers = increment_two_digits(last_entry.first_two_numbers)
                    if self.first_two_numbers == 100:
                        self.first_two_numbers = 0
                        self.first_two_letters = increment_two_letters(last_entry.first_two_letters)
                    else:
                        self.first_two_numbers = last_entry.first_two_numbers
                else:
                    self.first_two_letters = last_entry.first_two_letters
                    self.first_two_numbers = last_entry.first_two_numbers
            else:
                self.last_one_letter = last_entry.last_one_letter
                self.first_two_letters = last_entry.first_two_letters
                self.first_two_numbers = last_entry.first_two_numbers

            self.service_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.service_id = f"{self.prefix}-AA00A00"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        if not self.service_id:
            self.generate_id_number()
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Service.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Service, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Service, self).save(*args, **kwargs)


class Price(Main):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                blank=True, null=True, related_name='service_price_service')
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    is_range = models.BooleanField(default=False)
    location = models.ForeignKey(
        Destination, on_delete=models.SET_NULL, blank=True, null=True, related_name='location')
    duration_hour = models.CharField(
        max_length=128, choices=DURATION_HOUR_CHOICES, default='', blank=True, null=True)
    duration_minute = models.CharField(max_length=128, choices=DURATION_MINUTE_CHOICES, default='', blank=True,
                                       null=True)
    duration_day = models.CharField(
        max_length=128, choices=DURATION_DAY_CHOICES, default='', blank=True, null=True)
    time = models.CharField(
        max_length=128, choices=TIME_CHOICES, default='', blank=True, null=True)
    end_time = models.CharField(
        max_length=128, choices=TIME_CHOICES, default='', blank=True, null=True)
    day = models.CharField(max_length=128, choices=DAY_CHOICE,
                           default='', blank=True, null=True)
    end_day = models.CharField(
        max_length=128, choices=DAY_CHOICE, default='', blank=True, null=True)
    date = models.CharField(
        max_length=128, choices=DATE_CHOICES, default='', blank=True, null=True)
    end_date = models.CharField(
        max_length=128, choices=DATE_CHOICES, default='', blank=True, null=True)

    def __str__(self):
        return self.service.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Price.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Price, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Price, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'


class ServiceImage(Main):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_image")
    image = models.ImageField(upload_to="service/service/image")
    thumbnail = models.ImageField(
        upload_to="service/service/image", blank=True, null=True)
    is_thumbnail = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service Image"
        verbose_name_plural = "Service Images"

    def __str__(self):
        return (
            self.service.name
            if self.service and self.service.name
            else "No service name"
        )

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [ServiceImage.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(ServiceImage, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(ServiceImage, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = ServiceImage.objects.get(id=self.id)
            old_image = this_instance.image
        except ServiceImage.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(ServiceImage, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class ServiceReview(Main):
    is_active = models.BooleanField(default=True)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_service_review_service", )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name="service_service_review_user", )
    review_title = models.CharField(max_length=500, null=True, blank=True)
    review_summary = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True,
                                         blank=True, )
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name="service_service_review_replied_by")

    def __str__(self):
        return self.review_title if self.review_title else "No Title"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [ServiceReview.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(ServiceReview, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(ServiceReview, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("service", "user"),)
        ordering = ["-created_at"]
        verbose_name = "Service Review"
        verbose_name_plural = "Service Reviews"


class ServiceAvailability(Main):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,
                                related_name="service_service_availability_service")
    date = models.DateField()
    all_slots_available = models.BooleanField(default=False)
    time = models.JSONField(default=default_false_time_slot)

    class Meta:
        verbose_name = "Service Availability"
        verbose_name_plural = "Service Availabilities"

    def __str__(self):
        return self.service.name

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            # Get the data before the update
            data_before = serialize(
                'json', [ServiceAvailability.objects.get(pk=self.pk)]) or None

            # Call the original save method to save the instance
            super(ServiceAvailability, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            super(ServiceAvailability, self).save(*args, **kwargs)

        # Additional logic to handle time slot defaults
        if self.all_slots_available:
            self.time = default_true_time_slot()
            super(ServiceAvailability, self).save(*args, **kwargs)


class Package(Main):
    is_active = models.BooleanField(default=False)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_package_service")
    name = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    day = models.CharField(choices=DAY_CHOICES,
                           max_length=100, blank=True, null=True)
    night = models.CharField(
        choices=DAY_CHOICES, max_length=100, blank=True, null=True)
    capacity = models.PositiveIntegerField(default=0)
    image = models.FileField(upload_to="service/package/image")
    price = models.PositiveIntegerField(blank=True, null=True)
    # ID handling section
    prefix = models.CharField(max_length=10, default="SA-PKG")
    first_two_letters = models.CharField(max_length=2, default="AA")
    first_two_numbers = models.IntegerField(default=0)
    last_one_letter = models.CharField(max_length=1, default="A")
    last_two_numbers = models.IntegerField(default=0)
    package_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.package_id if self.package_id else "No Package ID"

    def generate_id_number(self):
        last_entry = Package.objects.order_by('-created_at').first()
        if last_entry:
            if last_entry.last_two_numbers == 99:
                self.last_one_letter = increment_one_letter(
                    last_entry.last_one_letter)
                # Reset last_two_numbers to 0 when last_one_letter is incremented
                self.last_two_numbers = 0
            else:
                self.last_one_letter = last_entry.last_one_letter
                self.last_two_numbers = last_entry.last_two_numbers + 1

            if self.last_one_letter in ['Z', 'z'] and self.last_two_numbers == 99:
                self.first_two_numbers = increment_two_digits(
                    last_entry.first_two_numbers)
                # Reset last_two_numbers to 0 when first_two_numbers is incremented
                self.last_two_numbers = 0
            else:
                self.first_two_numbers = last_entry.first_two_numbers

            if self.first_two_numbers == 99 and self.last_one_letter in ['Z', 'z'] and self.last_two_numbers == 99:
                self.first_two_letters = increment_two_letters(
                    last_entry.first_two_letters)
                # Reset first_two_numbers to 0 when first_two_letters is incremented
                self.first_two_numbers = 0
            else:
                self.first_two_letters = last_entry.first_two_letters

            self.last_two_numbers = increment_two_digits(self.last_two_numbers)

            self.package_id = f"{self.prefix}-{self.first_two_letters}{self.first_two_numbers:02d}{self.last_one_letter}{self.last_two_numbers:02d}"
        else:
            self.package_id = f"{self.prefix}-AA00A00"

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [Package.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Package, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Package, self).save(*args, **kwargs)

        if not self.package_id:
            self.generate_id_number()
        super(Package, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = Package.objects.get(id=self.id)
            old_image = this_instance.image
        except Package.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(Package, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        self.create_update_log(data_before, None)


class CapacityCount(Main):
    date = models.DateField(blank=True, null=True)
    service = models.ForeignKey(Service, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='service_capacitycount_service')
    package = models.ForeignKey(Package, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='service_capacitycount_package')

    def create_update_log(self, data_before, data_after):
        request = get_current_request()
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=request.user if request and hasattr(
                request, 'user') else None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize(
                    'json', [CapacityCount.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(CapacityCount, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            self.create_update_log(data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(CapacityCount, self).save(*args, **kwargs)

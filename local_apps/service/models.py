from django.db import models
from local_apps.company.models import Company
from local_apps.core.models import Main
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from local_apps.main.models import Category, SubCategory

DAY_CHOICES = [(i, str(i)) for i in range(1, 30)]

SERVICE_TYPE = (
    ("Service", "Service"),
    ("Activity", "Activity"),
)

PRICE_TYPE = (
    ("Ticket", "Ticket"),
    ("Day", "Day"),
    ("Item", "Item"),
)

OPERATION_TYPE = (
    ("One Way", "One Way"),
    ("Round Trip", "Round Trip"),
)


def default_timeslot():
    return [
        {'time': '00:00 am', 'slot': False},
        {'time': '01:00 am', 'slot': False},
        {'time': '02:00 am', 'slot': False},
        {'time': '03:00 am', 'slot': False},
        {'time': '04:00 am', 'slot': False},
        {'time': '05:00 am', 'slot': False},
        {'time': '06:00 am', 'slot': False},
        {'time': '07:00 am', 'slot': False},
        {'time': '08:00 am', 'slot': False},
        {'time': '09:00 am', 'slot': False},
        {'time': '10:00 am', 'slot': False},
        {'time': '11:00 am', 'slot': False},
        {'time': '12:00 pm', 'slot': False},
        {'time': '01:00 pm', 'slot': False},
        {'time': '02:00 pm', 'slot': False},
        {'time': '03:00 pm', 'slot': False},
        {'time': '04:00 pm', 'slot': False},
        {'time': '05:00 pm', 'slot': False},
        {'time': '06:00 pm', 'slot': False},
        {'time': '07:00 pm', 'slot': False},
        {'time': '08:00 pm', 'slot': False},
        {'time': '09:00 pm', 'slot': False},
        {'time': '10:00 pm', 'slot': False},
        {'time': '11:00 pm', 'slot': False},
    ]


class Destination(Main):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"


class ProfitMethod(Main):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Profit Method"
        verbose_name_plural = "Profit Methods"


class PriceCriterion(Main):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Profile Criterion"
        verbose_name_plural = "Profile Criterions"


class Duration(Main):
    time = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.time

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Duration"
        verbose_name_plural = "Durations"


class Price(Main):
    profile_method = models.ForeignKey(ProfitMethod, on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name='service_price_profile_method')
    price_criterion = models.ForeignKey(PriceCriterion, on_delete=models.SET_NULL, blank=True, null=True,
                                        related_name='service_price_price_criterion')
    price_per = models.CharField(
        choices=PRICE_TYPE, max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    sea_arabia_percentage = models.PositiveIntegerField(blank=True, null=True)
    vendor_percentage = models.PositiveIntegerField(blank=True, null=True)
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='service_price_duration')
    markup_fee = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.profile_method.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Price"
        verbose_name_plural = "Prices"


class PriceList(Main):
    price_map = models.ForeignKey(Price, on_delete=models.SET_NULL, blank=True, null=True,
                                  related_name='service_price_list_price_map')
    operation_type = models.CharField(choices=OPERATION_TYPE, default='Round Trip', max_length=100, blank=True,
                                      null=True)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='service_price_list_destination')
    duration = models.ForeignKey(Duration, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='service_price_list_duration')
    price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.destination.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Price List"
        verbose_name_plural = "Price List"


class Amenity(Main):
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.FileField(upload_to="service/amenity/image")

    def __str__(self):
        return self.name

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
    pickup_point = models.CharField(max_length=200, blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    refund_policy = models.TextField(blank=True, null=True)
    price = models.ForeignKey(
        Price, on_delete=models.CASCADE, related_name='service_service_price')
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name if self.name else "No Service Name"


class ServiceImage(Main):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_image")
    image = models.ImageField(upload_to="service/service/image")
    thumbnail = models.ImageField(
        upload_to="service/service/image", blank=True, null=True)
    is_thumbnail = models.BooleanField(default=False)

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


class ServiceReview(Main):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_title if self.review_title else "No Title"

    class Meta:
        unique_together = (("service", "user"),)
        ordering = ["-created_at"]
        verbose_name = "Service Review"
        verbose_name_plural = "Service Reviews"


class ServiceAvailability(Main):
    service = models.ForeignKey('Service', on_delete=models.CASCADE,
                                related_name="service_service_availability_service")
    date = models.DateField()
    time = models.JSONField(default=default_timeslot)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service Availability"
        verbose_name_plural = "Service Availabilities"


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

    def __str__(self):
        return self.name if self.name else "No Packages"

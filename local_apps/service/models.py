from django.db import models
from local_apps.company.models import Company
from local_apps.core.models import Main
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from local_apps.main.models import Category, SubCategory

NUMBER_CHOICES = []

for day_count in range(1, 15):
    one = f"{day_count} day{'s' if day_count > 1 else ''} and {day_count - 1} night{'s' if day_count - 1 > 1 else ''}"
    two = f"{day_count} day{'s' if day_count > 1 else ''} and {day_count} night{'s' if day_count > 1 else ''}"
    three = f"{day_count} day{'s' if day_count > 1 else ''} and {day_count + 1} night{'s' if day_count + 1 > 1 else ''}"
    NUMBER_CHOICES.append((one, one)) if day_count - 1 > 0 else NUMBER_CHOICES.append(
        ("1 day", "1 day")
    )
    NUMBER_CHOICES.append((two, two))
    NUMBER_CHOICES.append((three, three))

DAY_CHOICES = [(i, str(i)) for i in range(1, 30)]

SERVICE_TYPE = (
    ("Service", "Service"),
    ("Activity", "Activity"),
)

VENDOR_PRICE_TYPE = (
    ("Percentage", "Percentage"),
    ("Amount", "Amount"),
)

VENDOR_PERIOD_TYPE = (
    ("Per Service", "Per Service"),
    ("Monthly", "Monthly"),
    ("Yearly", "Yearly"),
    ("Per Ticket", "Per Ticket"),
)


class Occasion(Main):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Occasion"
        verbose_name_plural = "Occasions"

    def __str__(self):
        return self.name


class VendorPriceType(Main):
    name = models.CharField(max_length=255)
    type = models.CharField(
        choices=VENDOR_PRICE_TYPE,
        max_length=100,
        default="Amount",
        blank=True,
        null=True,
    )
    period = models.CharField(
        choices=VENDOR_PERIOD_TYPE,
        max_length=100,
        default="Per Service",
        blank=True,
        null=True,
    )
    vendor = models.PositiveIntegerField(blank=True, null=True)
    sea_arabia = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Vendor Price Type"
        verbose_name_plural = "Vendor Price Types"


class Destination(Main):
    name = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"


class Amenity(Main):
    name = models.CharField(max_length=255)
    image = models.FileField(upload_to="service/amenity/image", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"


# class Category(Main):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ["-created_at", "-updated_at"]
#         verbose_name = "Category"
#         verbose_name_plural = "Categories"


# class SubCategory(Main):
#     category = models.ForeignKey(
#         Category, on_delete=models.SET_NULL, blank=True, null=True
#     )
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ["-created_at", "-updated_at"]
#         verbose_name = "Sub Category"
#         verbose_name_plural = "Sub Categories"


class Service(Main):
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_top_suggestion = models.BooleanField(default=False)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(
        choices=SERVICE_TYPE, max_length=100, default="Service", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.SET_NULL, blank=True, null=True
    )
    occasions = models.ManyToManyField(Occasion, blank=True)
    other_type = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    machine_id = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pickup_point = models.CharField(max_length=200, blank=True, null=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.SET_NULL, blank=True, null=True
    )
    capacity = models.CharField(max_length=200, blank=True, null=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    day = models.CharField(
        choices=NUMBER_CHOICES, max_length=100, blank=True, null=True
    )
    night = models.CharField(
        choices=NUMBER_CHOICES, max_length=100, blank=True, null=True
    )
    pricing_type = models.ForeignKey(
        VendorPriceType, on_delete=models.SET_NULL, blank=True, null=True
    )
    default_price = models.PositiveIntegerField(blank=True, null=True)
    privacy_policy = models.FileField(
        upload_to="service/service/privacy_policy", blank=True, null=True
    )
    return_policy = models.FileField(
        upload_to="service/service/return_policy", blank=True, null=True
    )

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name if self.name else "No Service Name"

    # def save(self, *args, **kwargs):
    #     try:
    #         this_instance = Proposal.objects.get(id=self.id)
    #         old_file = this_instance.attachment
    #     except Proposal.DoesNotExist:
    #         old_file = None
    #
    #     super(Proposal, self).save(*args, **kwargs)
    #
    #     if old_file and self.attachment and old_file != self.attachment:
    #         remove_file(old_file)
    #
    # def delete(self, *args, **kwargs):
    #     if self.attachment:
    #         remove_file(self.attachment)
    #
    #     super(Proposal, self).delete(*args, **kwargs)


class Price(Main):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_price"
    )
    name = models.CharField(max_length=255, default="No Name")
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Price"
        verbose_name_plural = "Prices"

    def __str__(self):
        return self.name


class ServiceImage(Main):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="service_image"
    )
    image = models.ImageField(upload_to="service/service/image", blank=True, null=True)
    thumbnail = models.ImageField(
        upload_to="service/service/image", blank=True, null=True
    )
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
        Service,
        on_delete=models.CASCADE,
        related_name="service_service_review_service",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="service_service_review_user",
    )
    review_title = models.CharField(max_length=500, null=True, blank=True)
    review_summary = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="service_service_review_replied_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review_title if self.review_title else "No Title"

    class Meta:
        unique_together = (("service", "user"),)
        ordering = ["-created_at"]
        verbose_name = "Service Review"
        verbose_name_plural = "Service Reviews"

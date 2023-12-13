from django.db import models
from local_apps.main.models import Main
from local_apps.service.models import Service
from local_apps.company.models import Company

DISCOUNT_TYPE = (
    ('Fixed', 'Fixed'),
    ('Percentage', 'Percentage'),
)


class Offer(Main):
    is_enable = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='offer/offer/image', blank=True, null=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, max_length=25)
    discount_value = models.PositiveIntegerField(default=0, blank=True, null=True)
    max_redeem_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    max_redeem_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    min_grand_total = models.PositiveIntegerField(default=0, blank=True, null=True)
    allow_multiple_redeem = models.BooleanField(default=False)
    allow_global_redeem = models.BooleanField(default=False)
    display_global = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    services = models.ManyToManyField(Service, blank=True)
    companies = models.ManyToManyField(Company, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

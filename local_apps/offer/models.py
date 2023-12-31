from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import models
from local_apps.main.models import Main
from local_apps.service.models import Service
from local_apps.company.models import Company
from utils.file_handle import remove_file
from utils.model_logs import create_update_log

DISCOUNT_TYPE = (
    ('Fixed', 'Fixed'),
    ('Percentage', 'Percentage'),
)

MULTIPLE_REDEEM_TYPE = (('One-Time', 'One-Time'),
                        ('Multiple-time', 'Multiple-Time'))

REDEMPTION_TYPE = (('One-Time', 'One-Time'),
                   ('Unlimited', 'Unlimited'),
                   ('Limited-Number', 'Limited-Number'))

Expiration_TYPE =  (('No-Expiry', 'No-Expiry'),
                   ('Limited-Time', 'Limited-Time'))


class Offer(Main):
    is_enable = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='offer/offer/image', blank=True, null=True)
    discount_type = models.CharField(choices=DISCOUNT_TYPE, max_length=25, blank=True, null=True)
    discount_value = models.PositiveIntegerField(default=0, blank=True, null=True)
    up_to_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    redemption_type = models.CharField(choices=REDEMPTION_TYPE, max_length=25, blank=True, null=True)
    specify_no = models.PositiveIntegerField(default=0, blank=True, null=True)
    purchase_requirement = models.BooleanField(default=0, blank=True, null=True)
    min_purchase_amount = models.PositiveIntegerField(default=0, blank=True, null=True)
    allow_multiple_redeem = models.CharField(choices=MULTIPLE_REDEEM_TYPE, max_length=25, blank=True, null=True)
    multiple_redeem_specify_no = models.PositiveIntegerField(default=0, blank=True, null=True)
    expiration = models.CharField(choices=Expiration_TYPE, max_length=25, blank=True, null=True)
    on_home_screen = models.BooleanField(default=False)
    on_checkout = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_lifetime = models.BooleanField(default=False)
    services = models.ManyToManyField(Service, blank=True, related_name='offer_offer_services')
    companies = models.ManyToManyField(Company, blank=True, related_name='offer_offer_companies')
    apply_global = models.BooleanField(default=True)
    redeem_count = models.PositiveIntegerField(default=0, blank=True, null=True)
    multiple_redeem_count=models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Offer.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Offer, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            create_update_log(self, data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Offer, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = Offer.objects.get(id=self.id)
            old_image = this_instance.image
        except Offer.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(Offer, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        create_update_log(self, data_before, None)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from local_apps.api_report.middleware import get_current_request
from local_apps.api_report.models import ModelUpdateLog
from local_apps.main.models import Main
from utils.file_handle import remove_file
from utils.model_logs import create_update_log


class Advertisement(Main):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="advertisement/advertisement/image", null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "No Advertisement"

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Advertisement.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Advertisement, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            create_update_log(self, data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Advertisement, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = Advertisement.objects.get(id=self.id)
            old_image = this_instance.image
        except Advertisement.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(Advertisement, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        create_update_log(self, data_before, None)




from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from django.db import models
from local_apps.core.models import Main
from utils.file_handle import remove_file
from utils.model_logs import create_update_log


class Category(Main):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="main/category/image", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [Category.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(Category, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            create_update_log(self, data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(Category, self).save(*args, **kwargs)

        # Remove old image if it has changed
        try:
            this_instance = Category.objects.get(id=self.id)
            old_image = this_instance.image
        except Category.DoesNotExist:
            old_image = None

        if old_image and self.image and old_image != self.image:
            remove_file(old_image)

    def delete(self, *args, **kwargs):
        data_before = serialize('json', [self])  # Capture data before deletion
        if self.image:
            remove_file(self.image)

        super(Category, self).delete(*args, **kwargs)
        # Create a log entry after deletion
        create_update_log(self, data_before, None)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class SubCategory(Main):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the instance already exists
        if self.pk:
            try:
                # Get the data before the update
                data_before = serialize('json', [SubCategory.objects.get(pk=self.pk)])
            except ObjectDoesNotExist:
                # Instance doesn't exist yet, set data_before to None
                data_before = None

            # Call the original save method to save the instance
            super(SubCategory, self).save(*args, **kwargs)

            # Get the data after the update
            data_after = serialize('json', [self])

            # Create a log entry
            create_update_log(self, data_before, data_after)
        else:
            # Call the original save method to save the instance
            super(SubCategory, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

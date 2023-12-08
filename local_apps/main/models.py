from django.db import models
from local_apps.core.models import Main


class Category(Main):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="main/category/image",null=True,blank=True)

    def __str__(self):
        return self.name

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

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"

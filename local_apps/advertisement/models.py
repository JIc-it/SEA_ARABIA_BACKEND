from django.db import models
from local_apps.main.models import Main
# Create your models here.


class Advertisement(Main):
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to="advertisement/advertisement/image",null=True,blank=True)

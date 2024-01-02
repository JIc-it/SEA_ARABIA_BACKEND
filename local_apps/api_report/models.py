from django.db import models
from local_apps.account.models import User
from ckeditor.fields import RichTextField


class APILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='api_log_api_log_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    params = RichTextField(blank=True, null=True)
    headers = RichTextField(blank=True, null=True)
    request_data = RichTextField(blank=True, null=True)
    response_data = RichTextField(blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'

    def __str__(self):
        return self.url

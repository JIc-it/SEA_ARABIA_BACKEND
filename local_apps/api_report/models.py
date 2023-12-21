from django.db import models
from local_apps.account.models import User
from ckeditor.fields import RichTextField
from local_apps.core.models import Main


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
    

class ModelUpdateLog(models.Model):
    model_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.SET_NULL,
                             related_name='api_log_model_update_log_user')
    timestamp = models.DateTimeField(auto_now_add=True)
    data_before = models.TextField()
    data_after = models.TextField()

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = 'Model Update Log'
        verbose_name_plural = 'Model Update Logs'

    def __str__(self):
        return self.model_name
    

class ActionLog(Main):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='api_log_action_log_user')
    model_name = models.CharField(max_length=255, null=True, blank=True)
    action = models.CharField(max_length=255, null=True, blank=True)
    title = models.TextField(blank=True, null=True)
    value_before = models.JSONField(blank=True, null=True)
    value_after = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at", "-updated_at"]
        verbose_name = 'Action Log'
        verbose_name_plural = 'Action Logs'

    def __str__(self):
        return self.model_name
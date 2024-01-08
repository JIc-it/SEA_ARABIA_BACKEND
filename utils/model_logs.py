from django.utils import timezone
from local_apps.api_report.middleware import get_current_request
from local_apps.api_report.models import ModelUpdateLog


def create_update_log(self, data_before, data_after):
    request = get_current_request()
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=user,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )
    else:
        ModelUpdateLog.objects.create(
            model_name=self.__class__.__name__,
            user=None,
            timestamp=timezone.now(),
            data_before=data_before,
            data_after=data_after
        )

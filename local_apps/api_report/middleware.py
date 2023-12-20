import json
from django.urls import reverse
from .models import APILog, ModelUpdateLog
from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from django.db import transaction


class LogModelUpdatesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.log_model_updates(request.user)
        return response

    def log_model_updates(self, user):
        with transaction.atomic():
            for model in apps.get_models():
                if self.is_loggable_model(model):
                    self.log_changes(model, user)

    def is_loggable_model(self, model):
        # Customize this method to exclude specific models from logging
        excluded_models = ['ModelUpdateLog', 'APILog', 'Error', 'LogEntry', 'Theme']
        return issubclass(model, models.Model) and model.__name__ not in excluded_models

    def log_changes(self, model, user):
        instances = model.objects.all()
        if not instances:
            return

        data_before = {instance.pk: self.serialize_instance(instance) for instance in instances}
        model.objects.update()  # Use the update method to efficiently update all instances

        # Retrieve the updated instances
        instances = model.objects.filter(pk__in=data_before.keys())
        data_after = {instance.pk: self.serialize_instance(instance) for instance in instances}

        for pk, before, after in zip(data_before.keys(), data_before.values(), data_after.values()):
            if before != after:
                ModelUpdateLog.objects.create(
                    model_name=model.__name__,
                    user=user,
                    data_before=before,
                    data_after=after
                )

    def serialize_instance(self, instance):
        # Customize this method to serialize the instance data as needed
        # You can use serializers or any other method to convert the instance data to a string
        return str(instance)


# class LogModelUpdatesMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)
#         self.log_model_updates(request.user)
#         return response

#     def log_model_updates(self, user):
#         for model in apps.get_models():
#             if self.is_loggable_model(model):
#                 self.log_changes(model, user)

#     # def is_loggable_model(self, model):
#     #     # You can customize this method to exclude specific models from logging
#     #     return issubclass(model, models.Model)
#     def is_loggable_model(self, model):
#         # Customize this method to exclude specific models from logging
#         excluded_models = ['ModelUpdateLog', 'APILog', 'Error','LogEntry','Theme']
#         return issubclass(model, models.Model) and model.__name__ not in excluded_models

#     def log_changes(self, model, user):
#         for instance in model.objects.all():
#             data_before = str(instance)
#             instance.save()
#             data_after = str(instance)

#             ModelUpdateLog.objects.create(
#                 model_name=model.__name__,
#                 user=user,
#                 data_before=data_before,
#                 data_after=data_after
#             )


class APILogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_body = request.body
        response = self.get_response(request)

        if not request.path.startswith(reverse('admin:index')):
            if not request.path.startswith('/assets/'):
                try:
                    if request_body:
                        # request_data = request_body.decode('utf-8')
                        request_data = request_body
                    else:
                        request_data = None
                except json.JSONDecodeError as e:
                    request_data = str(e)

                response_data = response.content.decode('utf-8')

                get_params = dict(request.GET) if request.GET else None

                user = request.user if request.user.is_authenticated else None

                APILog.objects.create(
                    url=request.path,
                    method=request.method,
                    headers=dict(request.headers),
                    request_data=request_data,
                    response_data=response_data,
                    user=user,
                    params=get_params,

                )

        return response

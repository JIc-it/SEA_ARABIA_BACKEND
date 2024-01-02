import json
from django.urls import reverse
from .models import APILog


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

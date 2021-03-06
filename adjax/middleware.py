from json import dumps

from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin

from .views import DispatchError


class DispatchErrorMiddleware(MiddlewareMixin):
    """ Middleware for catching dispatch errors.
    """

    HTTP_STATUS = 422

    def process_exception(self, request, exception):
        if isinstance(exception, DispatchError):
            return HttpResponse(dumps({
                'error': True,
                'message': str(exception),
            }), content_type='application/json', status=self.HTTP_STATUS)


class CsrfEnforceMiddleware(MiddlewareMixin):
    """ Middleware that ensures a CSRF token cookie is sent.
    """

    def process_view(self, request, *args, **kwargs):
        get_token(request)

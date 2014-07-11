from json import dumps

from django.http import HttpResponse

from .views import DispatchError


class DispatchErrorMiddleware(object):
    """ Middleware for catching dispatch errors.
    """

    def process_exception(self, request, exception):
        if isinstance(exception, DispatchError):
            return HttpResponse(dumps({
                'error': True,
                'message': str(exception),
            }), content_type='application/json', status=422)

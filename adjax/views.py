from json import loads, dumps

from django.http import Http404, HttpResponse

from .conf import settings
from .registry import registry


class DispatchError(Exception):
    """ Error when dispatching to a view.
    """
    pass


def get_request_data(request):
    """ Get JSON encoded data from request body.
    """
    if request.method != 'POST':
        raise DispatchError('POST method required')

    try:
        data = loads(request.body.decode())
    except ValueError:
        raise DispatchError('Request body is not valid JSON')

    if type(data) != dict:
        raise DispatchError('Request body JSON is not an Object')

    return data


def get_response_content(data):
    """ Get JSON response content.
    """
    try:
        return dumps(data)
    except ValueError:
        raise DispatchError('View did not return a serializable value')


def dispatch(request, app, name):
    """ Dispatch request to corresponding view.
    """
    view = registry.get(app, name)
    if view is None:
        raise Http404()

    args, defaults = view.signature
    required = [arg for arg in args if arg not in defaults]
    kwargs = defaults.copy()
    kwargs.update(get_request_data(request))

    for arg in required:
        if arg not in kwargs:
            raise DispatchError("Argument '{0}' missing".format(arg))

    return HttpResponse(get_response_content(view.func(request, **kwargs)),
                        content_type='application/json')


def interface(request):
    """ Return client code for accessing views.
    """
    return HttpResponse(registry.render(), content_type=settings.CONTENT_TYPE)

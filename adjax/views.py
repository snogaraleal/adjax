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

    kwargs = get_request_data(request)

    args, defaults = view.signature
    missing = [arg for arg in args if (arg not in kwargs and
                                       arg not in defaults)]

    if missing:
        raise DispatchError('Required argument{0} {1} missing'.format(
            '' if len(missing) == 1 else 's',
            ', '.join(["'{0}'".format(arg) for arg in missing])))

    return HttpResponse(get_response_content(view.func(request, **kwargs)),
                        content_type='application/json')


def interface(request):
    """ Return client code for accessing views.
    """
    return HttpResponse(registry.render(), content_type=settings.CONTENT_TYPE)

from json import dumps

from django.http import Http404, HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe

from .conf import settings
from .importer import importer
from .registry import registry, View
from .serializer import serializer, ObjectType


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
        data = serializer.decode(request.body.decode())
    except ValueError:
        raise DispatchError('Request body is not valid JSON')

    if type(data) != dict:
        raise DispatchError('Request body JSON is not an Object')

    return data


def get_response_content(data):
    """ Get JSON response content.
    """
    try:
        return serializer.encode(data)
    except ValueError:
        raise DispatchError('View did not return a serializable value')


@importer.ensure_loaded
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
        raise DispatchError('Required argument{} {} missing'.format(
            '' if len(missing) == 1 else 's',
            ', '.join(["'{}'".format(arg) for arg in missing])))

    data = view.func(request, **kwargs)

    return HttpResponse(get_response_content(data),
                        content_type='application/json')


@importer.ensure_loaded
def interface(request):
    """ Return client code for accessing views.
    """
    return HttpResponse(loader.render_to_string(settings.TEMPLATE, {
        'variable': settings.VARIABLE,
        'data': mark_safe(dumps(settings.DATA)),
        'views': mark_safe(dumps(registry.views,
                                 default=View.dumps_default)),
        'type': ObjectType.TYPE,
    }), content_type=settings.CONTENT_TYPE)

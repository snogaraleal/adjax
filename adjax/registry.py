from collections import defaultdict
from inspect import getfullargspec

from django.core.urlresolvers import reverse


class View(object):
    """ Registered view.
    """

    def __init__(self, func, **kwargs):
        """ Initialize view from callable.
        """
        self.func = func

    @property
    def wrapped_func(self):
        """ Return wrapped function if the view function is decorated.
        """
        if hasattr(self.func, '__wrapped__'):
            return self.func.__wrapped__
        else:
            return self.func

    ###########
    # VIEW ID #
    ###########

    @property
    def app(self):
        """ Get view app.
        """
        return self.wrapped_func.__module__.split('.')[-2]

    @property
    def name(self):
        """ Get view name.
        """
        return self.wrapped_func.__name__

    ############
    # SETTINGS #
    ############

    @property
    def signature(self):
        """ Get view arguments and default values.
        """
        argspec = getfullargspec(self.wrapped_func)

        try:
            argspec.args.remove('request')
        except ValueError:
            raise TypeError(
                '{0}.{1} does not have request as first argument'.format(
                    self.app, self.name))

        defaults = {}
        if argspec.defaults:
            defaults = dict(zip(reversed(argspec.args),
                                reversed(argspec.defaults)))

        return argspec.args, defaults

    @property
    def url(self):
        """ Get URL for view.
        """
        return reverse('adjax.views.dispatch', args=(self.app, self.name))

    ########
    # DATA #
    ########

    def get_data(self):
        """ Get view information required by client.
        """
        args, defaults = self.signature
        return {
            'args': args,
            'defaults': defaults,
            'url': self.url,
        }

    @classmethod
    def dumps_default(cls, obj):
        """ Get data to use as JSON default.
        """
        if isinstance(obj, cls):
            return obj.get_data()
        else:
            return obj


class Registry(object):
    """ Registry for keeping all AJAX views.
    """

    def __init__(self):
        """ Initialize registry.
        """
        self.views = defaultdict(lambda: {})

    def register(self, value):
        """ Register view.
        """
        if not isinstance(value, View):
            view = View(value)
        else:
            view = value

        self.views[view.app][view.name] = view

        return value

    def get(self, app, name):
        """ Get registered view instance.
        """
        return self.views.get(app, {}).get(name)


registry = Registry()

from collections import defaultdict
from inspect import getargspec
from json import dumps

from django.core.urlresolvers import reverse
from django.template import loader
from django.utils.functional import cached_property
from django.utils.importlib import import_module

from .conf import settings


class View(object):
    """ Registered view.
    """

    def __init__(self, func, **kwargs):
        """ Initialize view from callable.
        """
        self.func = func

    @property
    def app(self):
        """ Get view app.
        """
        return self.func.__module__.split('.')[-2]

    @property
    def name(self):
        """ Get view name.
        """
        return self.func.__name__

    @property
    def signature(self):
        """ Get view arguments and default values.
        """
        argspec = getargspec(self.func)
        argspec.args.remove('request')

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
        """ Get function to use as JSON default.
        """
        if isinstance(obj, cls):
            return obj.get_data()
        else:
            return obj


class Importer(object):
    """ Helper class for importing from installed apps.
    """

    def __init__(self, module):
        """ Initialize importer for loading the specified module.
        """
        self.module = module
        self.loaded = False

    def load(self):
        """ Search for module in all installed apps.
        """
        from django.conf import settings

        for app in settings.INSTALLED_APPS:
            try:
                module = '.'.join([app, self.module])
                import_module(module)
            except ImportError:
                pass

        self.loaded = True

    def ensure_loaded(self):
        """ Make sure all existing modules are imported.
        """
        if not self.loaded:
            self.load()


class Registry(object):
    """ Registry for keeping all AJAX views.
    """

    def __init__(self, importer):
        """ Initialize registry.
        """
        self.views = defaultdict(lambda: {})
        self.importer = importer

    def register(self, view):
        """ Register a view.
        """
        if not isinstance(view, View):
            view = View(view)

        self.views[view.app][view.name] = view

    def get(self, app, name):
        """ Get registered view instance.
        """
        self.importer.ensure_loaded()
        return self.views.get(app, {}).get(name)

    def render(self):
        """ Render template to string.
        """
        self.importer.ensure_loaded()
        return loader.render_to_string(settings.TEMPLATE, {
            'views': dumps(dict(self.views), default=View.dumps_default),
            'data': dumps(settings.DATA),
        })


registry = Registry(Importer(settings.MODULE_NAME))


def register(view):
    """ Register view.
    """
    registry.register(view)

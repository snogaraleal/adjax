import six

if six.PY3:
    from importlib import import_module
else:
    from django.utils.importlib import import_module

from .conf import settings


class Importer(object):
    """ Helper class for importing from installed apps.
    """

    def __init__(self, *modules):
        """ Initialize importer for loading the specified module.
        """
        self.modules = modules
        self.loaded = False

    def load(self):
        """ Search for module in all installed apps.
        """
        from django.conf import settings

        for app in settings.INSTALLED_APPS:
            for module in self.modules:
                try:
                    module = '.'.join([app, module])
                    import_module(module)
                except ImportError:
                    pass

        self.loaded = True

    def ensure_loaded(self, value):
        """ Make sure all existing modules are imported.
        """
        if not self.loaded:
            self.load()
        return value


importer = Importer(settings.VIEWS_MODULE_NAME,
                    settings.TYPES_MODULE_NAME)

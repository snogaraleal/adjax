from django.conf import settings


def get_setting(name, default):
    """ Get setting by name.
    """
    return getattr(settings, 'ADJAX_{}'.format(name.upper()), default)


TEMPLATE = get_setting('template', 'adjax/interface')
VARIABLE = get_setting('variable', 'ADJAX')
DATA = get_setting('data', {})
CONTENT_TYPE = get_setting('content_type', 'application/javascript')
VIEWS_MODULE_NAME = get_setting('views_module_name', 'ajax')
TYPES_MODULE_NAME = get_setting('types_module_name', 'types')

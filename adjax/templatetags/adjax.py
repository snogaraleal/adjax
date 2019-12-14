from django import template

try:
    from django.contrib.staticfiles.templatetags.staticfiles import static
except ImportError:
    from django.templatetags.static import static

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from django.utils import safestring


register = template.Library()


def get_script_tag(source):
    """ Get HTML script tag with the specified source.
    """
    return '<script type="text/javascript" src="{}"></script>'.format(source)


def get_script_tags(*sources):
    """ Get one line of HTML script tags with the specified sources.
    """
    return ''.join([get_script_tag(source) for source in sources])


@register.simple_tag()
def adjax_scripts():
    """ Return HTML with scripts.
    """
    from adjax import views  # noqa
    return safestring.mark_safe(get_script_tags(static('adjax/base.js'),
                                                reverse('adjax_interface')))

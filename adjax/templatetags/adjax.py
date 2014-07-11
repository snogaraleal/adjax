from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse


register = template.Library()


def get_script_tag(source):
    """ Get HTML script tag with the specified source.
    """
    return '<script type="text/javascript" src="{0}"></script>'.format(source)


def get_script_tags(*sources):
    """ Get one line of HTML script tags with the specified sources.
    """
    return ''.join([get_script_tag(source) for source in sources])


@register.simple_tag()
def adjax_scripts():
    """ Return HTML with scripts.
    """
    return get_script_tags(static('adjax/base.js'),
                           reverse('adjax.views.interface'))

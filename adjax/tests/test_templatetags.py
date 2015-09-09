from django.test import TestCase
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse

from ..templatetags.adjax import (get_script_tag, get_script_tags,
                                  adjax_scripts)


class TemplateTagsTestCase(TestCase):

    def test_get_script_tag(self):
        """ Test script tag HTML.
        """
        source = 'https://cdn.com/source.js'
        expected_html = ('<script type="text/javascript" '
                         'src="{}"></script>').format(source)

        self.assertEqual(get_script_tag(source), expected_html)

    def test_get_script_tags(self):
        """ Test script tag HTML joining.
        """
        a_html = get_script_tag('a')
        b_html = get_script_tag('b')
        c_html = get_script_tag('c')

        self.assertEqual(get_script_tags('a', 'b', 'c'),
                         a_html + b_html + c_html)

    def test_adjax_scripts(self):
        """ Test adjax scripts template tag.
        """
        adjax_js_html = adjax_scripts()

        base_js_html = get_script_tag(static('adjax/base.js'))
        interface_js_html = get_script_tag(reverse('adjax.views.interface'))

        self.assertIn(base_js_html, adjax_js_html)
        self.assertIn(interface_js_html, adjax_js_html)

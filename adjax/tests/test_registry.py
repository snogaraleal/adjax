from django.test import TestCase

from ..registry import View, Registry


class ViewTestCase(TestCase):

    def test_app_name(self):
        """ Test app and view name properties.
        """

        def func(request):
            pass

        func.__module__ = 'myapp.views'

        view = View(func)

        self.assertEqual(view.app, 'myapp')
        self.assertEqual(view.name, 'func')

    def test_signature(self):
        """ Test signature property that specifies function arguments.
        """

        def func(request, a, b, c=1):
            pass

        view = View(func)
        args, defaults = view.signature

        self.assertEqual(args, ['a', 'b', 'c'])
        self.assertIn('c', defaults)
        self.assertEqual(defaults['c'], 1)

    def test_get_data(self):
        """ Test function interface data.
        """

        def func(request):
            pass

        view = View(func)
        data = view.get_data()

        self.assertIn('args', data)
        self.assertIn('defaults', data)
        self.assertIn('url', data)

        self.assertEqual(data['url'], view.url)

    def test_dumps_default(self):
        """ Test serialization function.
        """

        def func(request):
            pass

        view = View(func)

        self.assertEqual(View.dumps_default(None), None)
        self.assertEqual(View.dumps_default(view), view.get_data())


class RegistryTestCase(TestCase):

    def test_register(self):
        """ Test app and view name properties.
        """

        def func(request):
            pass

        func.__module__ = 'myapp.views'

        registry = Registry()
        registry.register(func)

        self.assertEqual(registry.get('myapp', 'func').func, func)

from django.test import TestCase
from django.http import HttpResponse

from ..views import DispatchError
from ..middleware import DispatchErrorMiddleware


class DispatchErrorMiddlewareTestCase(TestCase):

    def test_process_exception(self):
        """ Test process exception method.
        """

        self.assertIsInstance(DispatchErrorMiddleware().process_exception(
            None, DispatchError('error')), HttpResponse)

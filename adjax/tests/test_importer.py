from django.test import TestCase

from ..importer import Importer


class ImporterTestCase(TestCase):

    def test_load(self):
        """ Test that the loaded attribute is changed appropriately when the
        importer is loaded.
        """
        importer = Importer('module')
        self.assertFalse(importer.loaded)

        importer.load()
        self.assertTrue(importer.loaded)

    def test_ensure_loaded(self):
        """ Test that the load method is called when the importer is not
        loaded for a decorated function.
        """
        importer = Importer('module')
        self.assertFalse(importer.loaded)

        @importer.ensure_loaded
        def func_a():
            return 42

        self.assertEqual(func_a(), 42)
        self.assertTrue(importer.loaded)

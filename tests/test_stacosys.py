import unittest

from stacosys import __version__


class StacosysTestCase(unittest.TestCase):
    def test_version(self):
        self.assertEqual("3.2", __version__)

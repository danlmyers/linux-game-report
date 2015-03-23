import os
import steamcheck
import unittest

class WebTestCase(unittest.TestCase):
    def setUp(self):
        self.app = steamcheck.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        assert u"Hello I am working YAY!" in str(rv.data)

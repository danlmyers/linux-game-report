import os
import steamcheck
import unittest
import json

class WebTestCase(unittest.TestCase):
    def setUp(self):
        steamcheck.app.config['TESTING'] = True
        self.app = steamcheck.app.test_client()

    def test_root(self):
        rv = self.app.get('/')
        self.assertIn(u"Hello I am working YAY!", str(rv.data))

    def test_report(self):
        rv = self.app.get('/report/76561198044413311')
        report = json.loads(rv.data.decode('utf-8'))
        self.assertEqual('moird', report['steamuser'])
        self.assertTrue(report['games']['20']['linux'])

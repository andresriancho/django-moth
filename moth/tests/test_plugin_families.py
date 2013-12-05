import unittest

from moth.utils.plugin_families import get_plugin_families


class TestPluginFamilies(unittest.TestCase):
    def test_get_plugin_families(self):
        result = get_plugin_families()
        expected = set(['grep', 'audit', 'core', 'auth', 'bruteforce', 'crawl'])
        self.assertEqual(set(result), expected)
import unittest
import requests


class TestDockerBuild(unittest.TestCase):

    def test_home(self):
        # pylint: disable=E1103
        response = requests.get('http://127.0.0.1:8000/')

        self.assertIn('A set of vulnerable scripts', response.content)
        self.assertIn('<li><a href="/grep/">Grep</a></li>', response.content)
        self.assertIn('<li><a href="/audit/">Audit</a></li>', response.content)

    def test_https_about(self):
        # pylint: disable=E1103
        response = requests.get('https://127.0.0.1:8001/about/', verify=False)
        self.assertIn('This software is the evolution', response.content)

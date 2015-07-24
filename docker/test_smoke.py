import unittest
import requests

from requests.adapters import (HTTPAdapter, DEFAULT_POOLSIZE, DEFAULT_RETRIES,
                               DEFAULT_POOLBLOCK)
from requests.packages.urllib3.poolmanager import PoolManager
import ssl


class TLSv1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=DEFAULT_POOLBLOCK,
                         **pool_kwargs):
        self._pool_connections = connections
        self._pool_maxsize = maxsize
        self._pool_block = block

        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize,
                                       block=block, strict=True,
                                       ssl_version=ssl.PROTOCOL_TLSv1,
                                       **pool_kwargs)


class TestDockerBuild(unittest.TestCase):

    def test_home(self):
        # pylint: disable=E1103
        response = requests.get('http://127.0.0.1:8000/')

        self.assertIn('A set of vulnerable scripts', response.text)
        self.assertIn('<li><a href="/grep/">Grep</a></li>', response.content)
        self.assertIn('<li><a href="/audit/">Audit</a></li>', response.content)

    def test_https_about(self):
        # pylint: disable=E1103
        session = requests.Session()
        session.mount('https://', TLSv1Adapter())

        response = session.get('https://127.0.0.1:8001/about/', verify=False)
        self.assertIn('This software is the evolution', response.content)

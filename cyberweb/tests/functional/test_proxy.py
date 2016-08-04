from cyberweb.tests import *

class TestProxyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='proxy', action='index'))
        # Test response...

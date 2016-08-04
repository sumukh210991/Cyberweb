from cyberweb.tests import *

class TestGcemController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='gcem', action='index'))
        # Test response...

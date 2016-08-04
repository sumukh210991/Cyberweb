from cyberweb.tests import *

class TestPkiproxyController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='pkiproxy', action='index'))
        # Test response...

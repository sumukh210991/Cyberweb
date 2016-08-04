from cyberweb.tests import *

class TestGsicredsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='gsicreds', action='index'))
        # Test response...

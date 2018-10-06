from falcon import testing
from app import api


class StreetApiTest(testing.TestCase):

    def setUp(self):
        super(StreetApiTest, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = api.create()


class PathTestCase(StreetApiTest):

    def test_best_path(self):

        result = self.simulate_get('/best-path/-9.700183490221788,-35.77856130823369/-9.57257482426674,-35.70799463197329')

        print result
from falcon import testing
from app import api, StreetPathFinderApp


class StreetApiTest(testing.TestCase):

    def setUp(self):
        super(StreetApiTest, self).setUp()

        # Assume the hypothetical `myapp` package has a
        # function called `create()` to initialize and
        # return a `falcon.API` instance.
        self.app = StreetPathFinderApp()


class PathTestCase(StreetApiTest):

    def test_best_path(self):

        result = self.simulate_get('/best-path/-9.700183490221788,-35.77856130823369/-9.57257482426674,-35.70799463197329')

        json_data = result.json

        self.assertEqual(json_data[666], {'lat': -9.572272621655625, 'lng': -35.71018427884466})
        self.assertEqual(json_data[400], {'lat': -9.573223536957677, 'lng': -35.76904104845525})
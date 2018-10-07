from falcon import testing

from pathfinderapp.app import StreetPathFinderApp


class StreetApiTest(testing.TestCase):

    def setUp(self):
        super(StreetApiTest, self).setUp()

        self.app = StreetPathFinderApp()


class PathTestCase(StreetApiTest):

    def test_best_path(self):

        result = self.simulate_get('/best-path/-9.700183490221788,-35.77856130823369;-9.57257482426674,-35.70799463197329')

        json_data = result.json

        self.assertEqual(json_data['extra_points'][0], {'lat': -9.689855085943641, 'lng': -35.769740509888685})
        self.assertEqual(json_data['full_path'][200], {'lat': -9.639730424688105, 'lng': -35.73542051131252})
        self.assertEqual(json_data['full_path'][500], {'lat': -9.548899442727883, 'lng': -35.731854499586156})
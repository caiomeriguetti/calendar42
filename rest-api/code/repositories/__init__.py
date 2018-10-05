from db import default_db


class FeaturesRepository(object):

    def get_all_street_paths(self):
        street_db = default_db()
        features = street_db.features
        return features.find()


class PointsRepository(object):

    def get_nearest_point(self, point):
        street_db = default_db()
        points = street_db.points
        nearest_point = points.find_one({'location': {'$near': {
            '$geometry': {
                'type': "Point",
                'coordinates': [point.coords['lng'], point.coords['lat']]
            },
            '$maxDistance': 200000,
            '$minDistance': 0
        }}})

        print nearest_point

        return nearest_point


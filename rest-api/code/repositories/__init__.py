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
                'coordinates': [point['lng'], point['lat']]
            },
            '$maxDistance': 200000,
            '$minDistance': 0
        }}})

        return nearest_point

    def get_farthest_point(self, point):
        street_db = default_db()
        points = street_db.points
        farthest_point = points.find_one({'location': {'$near': {
            '$geometry': {
                'type': "Point",
                'coordinates': [point['lng'], point['lat']]
            },
            '$maxDistance': 500,
            '$minDistance': 0
        }}})

        return farthest_point




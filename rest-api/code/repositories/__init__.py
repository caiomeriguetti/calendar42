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

        return {'lng': nearest_point['location']['coordinates'][0], 'lat': nearest_point['location']['coordinates'][1]}

    def get_farthest_point(self, point):
        street_db = default_db()
        points = street_db.points
        farthest_point = points.find_one({'location': {'$near': {
            '$geometry': {
                'type': "Point",
                'coordinates': [point['lng'], point['lat']]
            },
            '$maxDistance': 2500,
            '$minDistance': 1500
        }}})

        return {'lng': farthest_point['location']['coordinates'][0], 'lat': farthest_point['location']['coordinates'][1]}




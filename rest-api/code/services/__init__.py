from db import default_db

class PlaceFinderService(object):

    def get_places_near(self, center):
        pass


class GraphBuilder(object):

    def build_graph(self):
        street_db = default_db()
        features = street_db.features
        features_data = features.find()

        print features_data

        for feature in features_data:
            coords = feature['geometry']['coords_dict']

            # find intersections

            for coord in coords:

                street_intersections = features.find({
                    'geometry.coords_dict': {
                        '$elemMatch':{
                            'lng': coord['lng'], 'lat': coord['lat']
                        }
                    }
                })

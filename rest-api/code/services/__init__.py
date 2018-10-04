from db import default_db


class Point(object):
    def __init__(self, coords):
        self.connections = {}
        self.coords = coords
        self.id = ':'.join([str(coords['lat']), str(coords['lng'])])

    def connect(self, p):
        p.connections[self.id] = self
        self.connections[p.id] = p

    def equals(self, p):
        return p.coords == self.coords


class GraphService(object):

    def get_maximun_path(self, start, end):
        pass

    def build_graph(self):
        street_db = default_db()
        features = street_db.features
        features_data = features.find()

        connections = {}

        for feature in features_data:
            coords = feature['geometry']['coords_dict']

            # find intersections
            last_point = None

            for coord in coords:
                p = Point(coord)

                if last_point:
                    last_point.connect(p)

                    if last_point.id not in connections:
                        connections[last_point.id] = {}

                    if p.id not in connections:
                        connections[p.id] = {}

                    connections[last_point.id][p.id] = p
                    connections[p.id][last_point.id] = last_point

                last_point = p


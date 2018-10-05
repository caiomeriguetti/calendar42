import math

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
        return p.coords['lat'] == self.coords['lat'] and p.coords['lng'] == self.coords['lng']


class Graph(object):
    connections = None
    costs = None

    def __init__(self, connections, costs):
        self.connections = connections
        self.costs = costs

    def contains(self, p):
        return p.id in self.connections


class GraphService(object):

    def get_nearest_point(self, point):

        street_db = default_db()
        points = street_db.points
        nearest_point = points.find_one({'location': {'$near': {
           '$geometry': {
              'type': "Point" ,
              'coordinates': [ point.coords['lng'] , point.coords['lat'] ]
           },
           '$maxDistance': 200000,
           '$minDistance': 0
        }}})

        print nearest_point

        return Point({'lng': nearest_point['location']['coordinates'][0], 'lat': nearest_point['location']['coordinates'][1]})

    def get_maximun_path(self, start, end):

        graph = self.build_graph()

        start_point = Point({'lat': start['lat'], 'lng': start['lng']})
        end_point = Point({'lat': end['lat'], 'lng': end['lng']})

        if not graph.contains(start_point):
            start_point = self.get_nearest_point(start_point)

        if not graph.contains(end_point):
            end_point = self.get_nearest_point(end_point)

        print graph.contains(start_point)

        connections = graph.connections

        queue = [([], start_point)]
        visited = {}

        while len(queue) > 0:

            current_item = queue.pop(0)
            current_point = current_item[1]

            if current_point.id in visited and visited[current_point.id] is True:
                continue

            visited[current_point.id] = True

            current_path = current_item[0]

            for conn in connections[current_point.id].keys():
                point = connections[current_point.id][conn]
                path = current_path + [point.coords]

                if point.equals(end_point):
                    # path found
                    return path

                queue.append((path, point))

    def get_distance(self, p1, p2):

        lon1 = p1.coords['lng']
        lon2 = p2.coords['lng']

        lat1 = p1.coords['lat']
        lat2 = p2.coords['lat']

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        R = 6371e3;

        a = math.pow(math.sin(dlat / 2), 2) + math.cos(lat1) * math.cos(lat2) * math.pow((math.sin(dlon / 2)), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = R * c

        return d

    def build_graph(self):
        street_db = default_db()
        features = street_db.features
        features_data = features.find()

        connections = {}
        costs = {}

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

                    if p.id not in costs:
                        costs[p.id] = {}

                    if last_point.id not in costs:
                        costs[last_point.id] = {}

                    distance = self.get_distance(last_point, p)

                    connections[last_point.id][p.id] = p
                    connections[p.id][last_point.id] = last_point

                    costs[last_point.id][p.id] = distance
                    costs[p.id][last_point.id] = distance

                last_point = p

        return Graph(connections, costs)


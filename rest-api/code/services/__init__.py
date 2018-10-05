import math

from repositories import FeaturesRepository, PointsRepository
from street_graph import Graph, Point


class GeomService(object):

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


class GraphService(object):

    def __init__(self):
        self.features_repo = FeaturesRepository()
        self.points_repo = PointsRepository()
        self.geom_service = GeomService()

    def get_nearest_point(self, point):

        nearest_point = self.points_repo.get_nearest_point(point)

        return Point({'lng': nearest_point['location']['coordinates'][0], 'lat': nearest_point['location']['coordinates'][1]})

    def get_maximun_path(self, start, end):

        graph = self.build_graph()

        start_point = Point({'lat': start['lat'], 'lng': start['lng']})
        end_point = Point({'lat': end['lat'], 'lng': end['lng']})

        if not graph.contains(start_point):
            start_point = self.get_nearest_point(start_point)

        if not graph.contains(end_point):
            end_point = self.get_nearest_point(end_point)

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

    def build_graph(self):

        features_data = self.features_repo.get_all_street_paths()

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

                    distance = self.geom_service.get_distance(last_point, p)

                    connections[last_point.id][p.id] = p
                    connections[p.id][last_point.id] = last_point

                    costs[last_point.id][p.id] = distance
                    costs[p.id][last_point.id] = distance

                last_point = p

        return Graph(connections, costs)


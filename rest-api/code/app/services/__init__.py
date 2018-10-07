import json
import math

from app.db import client, cache
from app.repositories import FeaturesRepository, PointsRepository
from app.models import Graph


class GeomService(object):

    def get_distance(self, p1, p2):

        lon1 = p1['lng']
        lon2 = p2['lng']

        lat1 = p1['lat']
        lat2 = p2['lat']

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

    def get_full_path(self, graph, points):

        full_path = []
        extra_points = []

        for i in range(1, len(points)):

            start = points[i - 1]
            end = points[i]

            longer_path = self.get_longer_path(graph, start, end)
            path = longer_path['path']
            extra_points.append(longer_path['extra_point'])

            full_path += path

        return {'full_path': full_path, 'extra_points': extra_points}

    def get_path(self, graph, start_point, end_point):

        # normalization of start and end points so that they become a point that exists in the database

        if not graph.contains(start_point):
            start_point = self.points_repo.get_nearest_point(start_point)

        if not graph.contains(end_point):
            end_point = self.points_repo.get_nearest_point(end_point)

        connections = graph.connections

        # walking through the graph to find a path

        queue = [([], start_point)]
        visited = {}

        while len(queue) > 0:

            current_item = queue.pop(0)
            current_point = current_item[1]

            current_point_id = graph.get_id(current_point)

            if current_point_id in visited and visited[current_point_id] is True:
                continue

            visited[current_point_id] = True

            current_path = current_item[0]

            for conn in connections[current_point_id].keys():
                point = connections[current_point_id][conn]
                path = current_path + [point]

                if graph.equals(point, end_point):
                    # path found
                    return path

                queue.append((path, point))

    def get_longer_path(self, graph, start_point, end_point):

        farthest_point = self.points_repo.get_farthest_point(start_point)

        path1 = self.get_path(graph, start_point, farthest_point)
        path2 = self.get_path(graph, farthest_point, end_point)

        return {'path': path1 + path2, 'extra_point': farthest_point}

    def _check_cache(self):

        cachedb = cache.client()
        cached_graph = cachedb.exists('graph_cache')

        if cached_graph:
            connections = json.loads(cachedb.hget('graph_cache', 'connections'))
            costs = json.loads(cachedb.hget('graph_cache', 'costs'))

            return Graph(connections, costs)

        return None

    def build_graph(self):

        cached_graph = self._check_cache()

        if cached_graph:
            return cached_graph

        features_data = self.features_repo.get_all_street_paths()

        connections = {}
        costs = {}

        for feature in features_data:
            coords = feature['geometry']['coords_dict']

            # find intersections
            last_point = None

            graph = Graph()

            for coord in coords:
                p = coord

                if last_point:

                    last_id = graph.get_id(last_point)
                    p_id = graph.get_id(p)

                    if last_id not in connections:
                        connections[last_id] = {}

                    if p_id not in connections:
                        connections[p_id] = {}

                    if p_id not in costs:
                        costs[p_id] = {}

                    if last_id not in costs:
                        costs[last_id] = {}

                    distance = self.geom_service.get_distance(last_point, p)

                    connections[last_id][p_id] = p
                    connections[p_id][last_id] = last_point

                    costs[last_id][p_id] = distance
                    costs[p_id][last_id] = distance

                last_point = p

        graph.set_connections(connections)
        graph.set_costs(costs)

        cachedb.hset('graph_cache', 'connections', json.dumps(connections))
        cachedb.hset('graph_cache', 'costs', json.dumps(costs))

        return graph


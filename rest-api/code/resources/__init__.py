import falcon
import json
from services import GraphService


class PathResource(object):

    def on_get(self, req, resp, points):

        graph_service = GraphService()

        points = points.split(';')

        graph = graph_service.build_graph()

        full_path = []
        extra_points = []

        for i in range(1, len(points)):

            p1 = points[i - 1]
            p2 = points[i]

            p1_coords = p1.split(',')
            p2_coords = p2.split(',')

            start = {'lng': float(p1_coords[1]), 'lat': float(p1_coords[0])}
            end = {'lng': float(p2_coords[1]), 'lat': float(p2_coords[0])}

            longer_path = graph_service.get_longer_path(graph, start, end)
            path = longer_path['path']
            extra_points.append(longer_path['extra_point'])

            full_path += path

        resp.body = json.dumps({'full_path': full_path, 'extra_points': extra_points})
        resp.status = falcon.HTTP_200
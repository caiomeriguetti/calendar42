import falcon
import json
from pathfinderapp.services import GraphService


class PathResource(object):

    def on_get(self, req, resp, points):

        graph_service = GraphService()

        points = points.split(';')

        graph = graph_service.build_graph()

        parsed_points = []
        for p in points:
            p = p.split(',')
            parsed_points.append({'lat': float(p[0]), 'lng': float(p[1])})

        result = graph_service.get_full_path(graph, parsed_points)

        resp.body = json.dumps(result)
        resp.status = falcon.HTTP_200
import falcon

from services import GraphBuilder


class PlacesResource(object):

    def on_get(self, req, resp):
        builder = GraphBuilder()

        builder.build_graph()

        resp.body="ok"
        resp.status=falcon.HTTP_200
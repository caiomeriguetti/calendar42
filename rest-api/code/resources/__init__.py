import falcon
import json
from services import GraphService


class PlacesResource(object):

    def on_get(self, req, resp):
        builder = GraphService()

        start = {'lng': -35.77856130823369, 'lat': -9.700183490221788}
        end = {'lng': -35.70799463197329, 'lat': -9.57257482426674}

        path = builder.get_maximun_path(start, end)

        resp.body=json.dumps(path)

        resp.status=falcon.HTTP_200
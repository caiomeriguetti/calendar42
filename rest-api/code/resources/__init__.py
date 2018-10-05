import falcon
import json
from services import GraphService


class PlacesResource(object):

    def on_get(self, req, resp, p1, p2):

        graph_service = GraphService()

        p1_coords = p1.split(',')
        p2_coords = p2.split(',')

        # start = {'lng': -35.77856130823369, 'lat': -9.700183490221788}
        # end = {'lng': -35.70799463197329, 'lat': -9.57257482426674}

        start = {'lng': float(p1_coords[1]), 'lat': float(p1_coords[0])}
        end = {'lng': float(p2_coords[1]), 'lat': float(p2_coords[0])}

        print "asdasdasd", start, end

        path = graph_service.get_maximun_path(start, end)

        resp.body = json.dumps(path)
        resp.status = falcon.HTTP_200
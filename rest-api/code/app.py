# -*- coding: utf-8 -*-
import falcon
from falcon_extensions import Request
from resources import PlacesResource

app = falcon.API(request_type=Request)
app.add_route('/best-path/{p1}/{p2}', PlacesResource())


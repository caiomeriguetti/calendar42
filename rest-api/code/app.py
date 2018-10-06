# -*- coding: utf-8 -*-
import falcon
from falcon_extensions import Request
from routes import add_routes

api = falcon.API(request_type=Request)

add_routes(api)


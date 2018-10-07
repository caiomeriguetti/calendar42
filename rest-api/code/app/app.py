# -*- coding: utf-8 -*-
import falcon
from falcon_extensions import Request
from app.routes import add_routes


class StreetPathFinderApp(falcon.API):

    def __init__(self, *args, **kwargs):

        super(StreetPathFinderApp, self).__init__(request_type=Request, *args, **kwargs)

        add_routes(self)


app = StreetPathFinderApp()



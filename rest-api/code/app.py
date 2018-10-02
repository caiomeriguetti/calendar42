# -*- coding: utf-8 -*-
import falcon
from falcon_extensions import Request

app = falcon.API(request_type=Request)


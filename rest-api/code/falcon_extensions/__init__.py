# -*- coding: utf-8 -*-
from falcon.request import Request as FalconRequest
import json


class Request(FalconRequest):

    payload = None
    body = None

    def load_body_as_json(self):
        if self.body is not None:
            return self.body

        self.payload = self.stream.read()
        self.body = json.loads(self.payload.decode('utf-8'))

        return self.body

    def get_param_from_body(self, param):
        body = self.load_body_as_json()

        return None if param not in body else body[param]

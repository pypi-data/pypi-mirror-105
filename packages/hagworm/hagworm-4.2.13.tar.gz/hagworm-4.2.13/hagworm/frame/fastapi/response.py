# -*- coding: utf-8 -*-

from fastapi.responses import UJSONResponse

from hagworm.extend.struct import Result


class Response(UJSONResponse):

    def render(self, content):
        return super().render(Result(data=content))


class ErrorResponse(UJSONResponse, Exception):

    def __init__(self, error_code, content=None, status_code=200, **kwargs):

        self.error_code = error_code

        UJSONResponse.__init__(self, content, status_code, **kwargs)
        Exception.__init__(self, self.body.decode())

    def render(self, content):
        return super().render(Result(code=self.error_code, data=content))

from rest_framework.exceptions import APIException


class ImproperInput(Exception):
    pass


class VariableError(Exception):
    pass


class InvalidParameterError(APIException):
    def __init__(self, detail=None):
        super().__init__(detail=detail)
        self.status_code = 403

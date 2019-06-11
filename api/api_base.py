import copy
from api.core.exceptions import VariableError


class ApiBase(object):
    """Don't know how to do this yet"""
    accept = []
    accept_option = []
    mutual_exclusion = []
    variable_error_message = ""

    @classmethod
    def variable_check(cls, the_get):

        for v in cls.accept:
            if v not in the_get:
                raise VariableError(cls.variable_error_message)

        for v_p in cls.mutual_exclusion:
            the_count = 0
            for v in v_p:
                if v in the_get:
                    the_count += 1
                if the_count > 1:
                    raise VariableError(cls.variable_error_message)
        return True

    @classmethod
    def generate_input_argument(cls, the_get):
        input_dict = dict()
        for v in cls.accept:
            input_dict[v] = the_get[v]
        for v in cls.accept_option:
            input_dict[v] = the_get[v]
        return input_dict

    @staticmethod
    def call_function(func, **kwargs):
        return func(**kwargs)

    @classmethod
    def api_get(cls, request, func):
        the_get = copy.deepcopy(request.GET)
        if ApiBase.variable_check(the_get):
            kwargs = cls.generate_input_argument(the_get)
            return ApiBase.call_function(func, **kwargs)

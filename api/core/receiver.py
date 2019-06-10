import copy
import json

from django.core.exceptions import ObjectDoesNotExist
from api.core.exceptions import VariableError
from api.core.json_maker import convert_model_to_dict_simple, convert_model_to_dict_recursive
from django.http import HttpResponse

# for security reason this function is banned to use recursive function
RECURSIVE_BAN_FUN = ['get_platform_deployment_comments']


def receiver(func):
    def wrapper(request):
        json_obj = dict()
        json_obj['data'] = []
        the_get = copy.deepcopy(request.GET)
        recursive = the_get.pop('recursive', False)
        debug = the_get.pop('debug', False)
        try:
            model_res = func(request)
        except VariableError as e:
            if debug:
                error = "Given incorrect variable {function_name}: {reason}".format(function_name=func.__name__,
                                                                                    reason=e)
                return HttpResponse(json.dumps(error), content_type='application/json')
            else:
                return HttpResponse(json.dumps(json_obj), content_type='application/json', status=400)
        except ObjectDoesNotExist as e:
            if debug:
                error = "{function_name}: {reason}".format(function_name=func.__name__, reason=e)
                return HttpResponse(json.dumps(error), content_type='application/json', status=400)
            else:
                return HttpResponse(json.dumps(json_obj), content_type='application/json')
        except Exception as e:
            if debug:
                error = "{function_name}: {reason}".format(function_name=func.__name__, reason=e)
                return HttpResponse(json.dumps(error), content_type='application/json', status=400)
            else:
                return HttpResponse(json.dumps(json_obj), content_type='application/json', status=400)

        model_convert_function = convert_model_to_dict_simple
        if recursive and func.__name__ not in RECURSIVE_BAN_FUN:
            if type(recursive) is list:
                if recursive[0].lower() == 'true':
                    model_convert_function = convert_model_to_dict_recursive

        if type(model_res) == list:
            res = []
            for m in model_res:
                res.append(model_convert_function(m))
        else:
            res = model_convert_function(model_res)
        json_obj['data'] = res
        return HttpResponse(json.dumps(json_obj), content_type='application/json', status=200)

    return wrapper

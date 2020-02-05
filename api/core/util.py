from functools import lru_cache
from datetime import datetime
from django.apps import apps
from django.conf import settings

CASE_IN_SENSITIVE_FILTER_SUFFIX = '__iexact'


def filter_objs(objs, way_to_filter):
    new_objs = []
    for o in objs:
        if way_to_filter(o):
            new_objs.append(o)

    return new_objs


def no_none_dict(value):
    the_dict = dict()
    for x in value:
        if x and value[x]:
            the_dict[x] = value[x]
    return the_dict


INVALID_TIME_FORMAT = 0
YEAR_SEC = 1
YEAR_DAY = 2
year_sec_time_format = "%Y-%m-%d %H:%M:%S"
time_day_format = "%Y-%m-%d"


def time_format_identifier(time):
    try:
        datetime.strptime(time, year_sec_time_format)
    except Exception:
        try:
            datetime.strptime(time, time_day_format)
        except Exception:
            return INVALID_TIME_FORMAT
        else:
            return YEAR_DAY
    else:
        return YEAR_SEC


def time_to_time_range(time):
    return time + " 00:00:00", time + " 23:59:59"


def get_model_name(app_names):
    all_model_name = []
    for name in app_names:
        all_model_name.extend(apps.all_models[name])
    return all_model_name


@lru_cache(maxsize=None)
def get_all_model_name():
    return get_model_name(settings.LOCAL_APPS)


def change_to_case_insensitive_parameter(parameter_dictionary, parameter_alter_list=None):
    """ Covert diction key to key + __iexact
    if given parameter_alter_list, only alter the variables in list other wise covert all of it
    :param parameter_dictionary: diction input
    :param parameter_alter_list: variable list
    :return: dictionary
    """
    new_parameter_dictionary = dict()
    if parameter_alter_list is None:
        parameter_alter_list = parameter_dictionary.keys()
    else:
        if type(parameter_alter_list) != list:
            raise AttributeError("parameter_alter_list: {} should be list".format(
                parameter_alter_list))
    for key, item in parameter_dictionary.items():
        if key in parameter_alter_list:
            new_parameter_dictionary[key + CASE_IN_SENSITIVE_FILTER_SUFFIX] = item
        else:
            new_parameter_dictionary[key] = item
    return new_parameter_dictionary

from functools import lru_cache
from datetime import datetime
from django.apps import apps
from django.conf import settings


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

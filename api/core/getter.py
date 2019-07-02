import re

from platforms.models import *
from instruments.models import *
from general.models import *
from django.core.exceptions import ObjectDoesNotExist
from api.core.exceptions import ImproperInput


def get_platform_by_name(platform_name=None):
    platform_obj = None
    try:
        platform_obj = Platform.objects.get(name=platform_name)
    except ObjectDoesNotExist:
        pass
    finally:
        return platform_obj


def get_instrument_on_platform_by_platform(platform_name=None):
    res = []
    platform_obj = get_platform_by_name(platform_name)
    if not platform_obj:
        return res

    instrument_on_platform_objs = list(InstrumentOnPlatform.objects.filter(platform=platform_obj))

    return instrument_on_platform_objs


def get_instrument_by_platform(platform_name=None):
    instrument_on_platform_objs = get_instrument_on_platform_by_platform(platform_name)
    instrument_obj_list = []
    for a in instrument_on_platform_objs:
        instrument_obj_list.append(a.instrument)
    return instrument_obj_list


def get_sensors_by_platform(platform_name=None, output=True):
    sensor_list = []
    try:
        platform_obj = Platform.objects.get(name=platform_name)
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist("No platform name match {}".format(platform_name))

    instrument_on_platform_qs = InstrumentOnPlatform.objects.filter(platform=platform_obj)
    instrument_list = []
    for obj in instrument_on_platform_qs:
        instrument_list.append(obj.instrument)

    for obj in instrument_list:
        sensor_list.extend(list(Sensor.objects.filter(instrument=obj, include_in_output=output)))

    return sensor_list


def get_deployment_by_platform_name_start_time(platform_name=None, start_time=None):
    platform_obj = get_platform_by_name(
        platform_name
    )
    if not platform_obj:
        return None
    try:
        deployment_obj = PlatformDeployment.objects.get(platform=platform_obj, start_time=start_time)
    except ObjectDoesNotExist:
        return None
    return deployment_obj


def get_deployments_by_platform_name(platform_name=None):
    platform_obj = get_platform_by_name(
        platform_name
    )

    deployment_objs = PlatformDeployment.objects.filter(platform=platform_obj)

    return list(deployment_objs)


def get_sensors_by_deployment(platform_name=None, start_time=None, output=True):
    instrument_on_platforms = get_instrument_on_platform_by_platform(platform_name)
    filter_instrument_on_platforms = []
    deployment_obj = get_deployment_by_platform_name_start_time(platform_name, start_time)
    start_time = deployment_obj.start_time
    end_time = deployment_obj.end_time
    for i in instrument_on_platforms:
        if start_time >= i.start_time:
            if end_time:
                if i.end_time >= end_time:
                    filter_instrument_on_platforms.append(i)
            else:
                filter_instrument_on_platforms.append(i)
    sensor_list = []
    instruments = []
    for obj in filter_instrument_on_platforms:
        instruments.append(obj.instrument)

    for obj in instruments:
        sensor_list.extend(list(Sensor.objects.filter(instrument=obj, include_in_output=output)))

    return sensor_list


def filter_objs(objs, way_to_filter):
    new_objs = []
    for o in objs:
        if way_to_filter(o):
            new_objs.append(o)

    return new_objs


def get_platform_type(model=None, how="match"):
    # ["match", "contains", "regex"]
    # all exceptions will be handled in upper level

    try:
        lower_how = how.lower()
    except AttributeError:
        raise AttributeError("Invalid model")

    if lower_how == "match":
        try:
            platform_model_obj = PlatformType.objects.get(model=model)
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist(
                "Could no find exact match for model {}, you can set how = contains for partial match or"
                " set how = regex for Regular Expression match".format(
                    model))
        else:
            objs = [platform_model_obj]
    elif lower_how == 'contains':
        all_objs_query = PlatformType.objects.all()

        def filter_fun(obj):
            try:
                return (model.lower()) in obj.model.lower()
            except AttributeError:
                raise AttributeError("Invalid model")

        objs = filter_objs(all_objs_query,
                           filter_fun
                           )
    elif lower_how == 'regex':
        all_objs_query = PlatformType.objects.all()

        def filter_fun(obj):
            name = obj.model
            try:
                if re.match(model, name):
                    return True
                else:
                    return False
            except TypeError:
                raise TypeError("Invalid regex format")

        objs = filter_objs(all_objs_query,
                           filter_fun
                           )
    else:
        raise ImproperInput("how should be match or contains or regex")

    return objs


def get_platform_by_platform_type(model=None, how="match"):
    # ["match", "contains", "regex"]
    # all exceptions will be handled in upper level
    platform_types = get_platform_type(model, how)
    platform_objs = []
    for platform_type in platform_types:
        platform_objs.extend(list(Platform.objects.filter(platform_type=platform_type)))
    return platform_objs


def get_deployments_by_platform(platform_name=None):
    deployment_objs = []
    platform_obj = get_platform_by_name(platform_name)

    if platform_obj:
        deployment_objs = list(PlatformDeployment.objects.filter(platform=platform_obj))
    return deployment_objs


def get_deployments_by_platform_type(model=None, how="match"):
    platform_objs = get_platform_by_platform_type(model, how=how)
    deployment_obj_list = []
    for obj in platform_objs:
        deployment_objs = PlatformDeployment.objects.filter(platform=obj)
        if deployment_objs:
            deployment_obj_list.extend(list(deployment_objs))
    return deployment_obj_list


def get_instruments_by_deployment(platform_name=None, start_time=None):
    instrument_objs = []
    instrument_on_platform_objs = get_instrument_on_platform_by_platform(platform_name)
    if instrument_on_platform_objs:
        deployment_obj = get_deployment_by_platform_name_start_time(platform_name, start_time)
        start_t = deployment_obj.start_time
        end_t = deployment_obj.end_time
        for o in instrument_on_platform_objs:
            if start_t >= o.start_time:
                if end_t and o.end_time:
                    if end_t <= o.end_time:
                        instrument_objs.append(o.instrument)
                else:
                    instrument_objs.append(o.instrument)

    return instrument_objs


def get_deployment_comment(platform_name=None, start_time=None):
    deployment_obj = get_deployment_by_platform_name_start_time(platform_name, start_time)
    deployment_comment_box = PlatformDeploymentCommentBox.objects.get(platform_deployment=deployment_obj)
    deployment_comments = list(
        PlatformDeploymentComment.objects.filter(platform_deployment_comment_box=deployment_comment_box))
    return deployment_comments


def no_none_dict(value):
    the_dict = dict()
    for x in value:
        if x and value[x]:
            the_dict[x] = value[x]
    return the_dict


def get_instruments(identifier=None, short_name=None, long_name=None, serial=None):
    if not (identifier or short_name or long_name or serial):
        return Instrument.objects.all()
    else:
        the_dict = {
            "identifier": identifier,
            "short_name": short_name,
            "long_name": long_name,
            "serial": serial
        }
        the_dict = no_none_dict(the_dict)
        res = Instrument.objects.filter(**the_dict)
        return list(res)


def get_sensors(identifier=None, standard_name=None, long_name=None):
    if not (identifier, standard_name, long_name):
        return Sensor.objects.all()
    else:
        the_dict = {
            "identifier": identifier,
            "short_name": standard_name,
            "long_name": long_name
        }
        the_dict = no_none_dict(the_dict)
        res = Sensor.objects.filter(**the_dict)
        return list(res)


def get_platform(platform_name=None, serial_number=None):
    if not (platform_name, serial_number):
        return Platform.objects.all()
    else:
        the_dict = {
            "platform_name": platform_name,
            "serial_number": serial_number
        }
        the_dict = no_none_dict(the_dict)
        res = Platform.objects.filter(**the_dict)
        return list(res)


def get_manufacturer(name=None):
    if not name:
        return Manufacturer.objects.all()
    else:
        res = Manufacturer.objects.filter(name=name)
        return list(res)


def get_institutions(name=None):
    if not name:
        return Institution.objects.all()
    else:
        res = Institution.objects.filter(name=name)
        return list(res)


def get_project(name=None):
    if not name:
        return Project.objects.all()
    else:
        res = Project.objects.filter(name=name)
        return list(res)


def get_power(name=None):
    if not name:
        return PlatformPowerType.objects.all()
    else:
        res = PlatformPowerType.objects.filter(name=name)
        return list(res)

import re

from platforms.models import *
from instruments.models import *
from general.models import *
from django.core.exceptions import ObjectDoesNotExist
from api.core.exceptions import ImproperInput
from api.core.decorator import query_optimize_decorator
from django.db.models import Q


def get_platform_by_name(platform_name=None):
    platform_obj = Platform.objects.filter(name=platform_name)

    return platform_obj


def get_instrument_on_platform_by_platform(platform_name=None):
    res = []
    platform_obj = get_platform_by_name(platform_name)
    if not platform_obj:
        return res

    instrument_on_platform_objs = list(InstrumentOnPlatform.objects.filter(platform=platform_obj))

    return instrument_on_platform_objs


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

    deployment_queryset = PlatformDeployment.objects.filter(platform=platform_obj, start_time=start_time)

    return deployment_queryset


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


def get_deployments_by_platform(platform_name=None):
    deployment_objs = []
    platform_obj = get_platform_by_name(platform_name)

    if platform_obj:
        deployment_objs = list(PlatformDeployment.objects.filter(platform=platform_obj))
    return deployment_objs


def no_none_dict(value):
    the_dict = dict()
    for x in value:
        if x and value[x]:
            the_dict[x] = value[x]
    return the_dict


class GetQuerySetMethod:

    @staticmethod
    @query_optimize_decorator(['instrument'])
    def get_sensors(identifier=None, standard_name=None, long_name=None):
        if not any([identifier, standard_name, long_name]):
            qs = Sensor.objects.all()
        else:
            the_dict = {
                "identifier": identifier,
                "short_name": standard_name,
                "long_name": long_name
            }
            the_dict = no_none_dict(the_dict)
            qs = Sensor.objects.filter(**the_dict)
        return qs

    @staticmethod
    @query_optimize_decorator(['platform_type', 'institution'])
    def get_platforms(platform_name=None, serial_number=None):
        # todo: Figure out why when depth = 0, there is some duplicated queries
        if not any([platform_name, serial_number]):
            qs = Platform.objects.all()
        else:
            the_dict = {
                "name": platform_name,
                "serial_number": serial_number
            }
            the_dict = no_none_dict(the_dict)
            qs = Platform.objects.filter(**the_dict)

        return qs

    @staticmethod
    def get_platform(_, platform_name=None, serial_number=None, model=None, how="match", **kwargs):
        if model:
            qs = GetQuerySetMethod.get_platform_by_platform_type(model=model, how=how, **kwargs)
        else:
            qs = GetQuerySetMethod.get_platforms(platform_name=platform_name, serial_number=serial_number, **kwargs)
        return qs

    @staticmethod
    @query_optimize_decorator()
    def get_platform_by_platform_type(model=None, how="match"):
        # ["match", "contains", "regex"]
        # all exceptions will be handled in upper level
        if model is None:
            qs = Platform.objects.all()
        else:
            platform_types = get_platform_type(model, how)
            if platform_types:
                q_obj = Q(platform_type=platform_types[0])
                for i in range(1, len(platform_types)):
                    q_obj = q_obj | Q(platform_type=platform_types[i])

                qs = Platform.objects.filter(q_obj)
            else:
                qs = Platform.objects.none()
        return qs

    @staticmethod
    @query_optimize_decorator()
    def get_manufacturer(name=None):
        if not name:
            return Manufacturer.objects.all()
        else:
            res = Manufacturer.objects.filter(name=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_institutions(name=None):
        if not name:
            return Institution.objects.all()
        else:
            res = Institution.objects.filter(name=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_project(name=None):
        if not name:
            return Project.objects.all()
        else:
            res = Project.objects.filter(name=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_power(name=None):
        if not name:
            qs = PlatformPowerType.objects.all()
        else:
            qs = PlatformPowerType.objects.filter(name=name)
        return qs

    @staticmethod
    @query_optimize_decorator(["platform", "institution", "project", "power_type"])
    def get_deployments_by_platform_type(model=None, how="match"):
        platform_qs = GetQuerySetMethod.get_platform_by_platform_type(model=model, how=how)
        platform_pk_list = []
        for o in platform_qs:
            platform_pk_list.append(o.id)
        qs = PlatformDeployment.objects.filter(platform__pk__in=platform_pk_list)
        return qs

    @staticmethod
    @query_optimize_decorator(["platform", "institution", "project", "power_type"])
    def get_deployments(wmo_id=None, platform_name=None, institution_name=None, project_name=None, title=None,
                        testing_mission=None,
                        start_time=None, deployment_number=None):
        the_dict = {
            "wmo_id": wmo_id,
            "platform__name": platform_name,
            "institution__name": institution_name,
            "project__name": project_name,
            "title": title,
            "testing_mission": testing_mission,
            "start_time": start_time,
            "deployment_number": deployment_number
        }
        if not any(the_dict.values()):
            qs = PlatformDeployment.objects.all()
        else:
            # create for day range search when not providing full date detail
            the_dict = no_none_dict(the_dict)
            qs = PlatformDeployment.objects.filter(**the_dict)
        return qs

    @staticmethod
    def get_deployment(_, wmo_id=None, platform_name=None, institution_name=None, project_name=None, title=None,
                       testing_mission=None,
                       start_time=None, deployment_number=None, model=None, how='match', **kwargs):
        if model is not None:
            qs = GetQuerySetMethod.get_deployments_by_platform_type(model=model, how=how, **kwargs)
        else:
            qs = GetQuerySetMethod.get_deployments(wmo_id=wmo_id,
                                                   platform_name=platform_name,
                                                   institution_name=institution_name,
                                                   project_name=project_name,
                                                   title=title,
                                                   testing_mission=testing_mission,
                                                   start_time=start_time,
                                                   deployment_number=deployment_number,
                                                   **kwargs)
        return qs

    @staticmethod
    @query_optimize_decorator()
    def get_deployment_comment(platform=None, start_time=None):
        # query optimize problem
        if not any([platform, start_time]):
            qs = PlatformDeploymentComment.objects.all()
        else:
            deployment_qs = GetQuerySetMethod.get_deployment(platform_name=platform, start_time=start_time)
            deployment_objs = list(deployment_qs)
            if deployment_objs:
                deployment_obj = deployment_objs[0]
                deployment_comment_box = PlatformDeploymentCommentBox.objects.get(platform_deployment=deployment_obj)
                qs = PlatformDeploymentComment.objects.filter(
                    platform_deployment_comment_box=deployment_comment_box)
            else:
                qs = PlatformDeploymentComment.objects.none()
        return qs

    @staticmethod
    @query_optimize_decorator(['manufacturer'])
    def get_instrument_by_platform(platform_name=None):
        qs = InstrumentOnPlatform.objects.filter(platform__name=platform_name).prefetch_related('instrument')
        instrument_on_platform_objs = list(qs)
        pk_list = []
        for o in instrument_on_platform_objs:
            pk_list.append(o.instrument.id)

        qs = Instrument.objects.filter(pk__in=pk_list)

        return qs

    @staticmethod
    @query_optimize_decorator(['manufacturer'])
    def get_instrument(identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None):
        if not (identifier or short_name or long_name or serial):
            qs = Instrument.objects.all()
        else:
            the_dict = {
                "identifier": identifier,
                "short_name": short_name,
                "long_name": long_name,
                "serial": serial,
                "manufacturer__name": manufacturer
            }
            the_dict = no_none_dict(the_dict)
            res = Instrument.objects.filter(**the_dict)
            qs = res
        return qs

    @staticmethod
    @query_optimize_decorator()
    def get_instruments_by_deployment(platform_name=None, start_time=None):
        pk_list = []
        instrument_on_platform_objs = get_instrument_on_platform_by_platform(platform_name)
        if instrument_on_platform_objs:
            deployment_obj = get_deployment_by_platform_name_start_time(platform_name, start_time)
            start_t = deployment_obj.start_time
            end_t = deployment_obj.end_time
            for o in instrument_on_platform_objs:
                if start_t >= o.start_time:
                    if end_t and o.end_time:
                        if end_t <= o.end_time:
                            pk_list.append(o.instrument.id)
                    else:
                        pk_list.append(o.instrument.id)

        return Instrument.objects.filter(pk__in=pk_list)

    @staticmethod
    def get_instruments(_, identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None,
                        platform_name=None, start_time=None, **kwargs):

        if platform_name:
            if start_time:
                qs = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name, start_time=start_time,
                                                                     **kwargs)
            else:
                qs = GetQuerySetMethod.get_instrument_by_platform(platform_name=platform_name, **kwargs)
        else:
            qs = GetQuerySetMethod.get_instrument(identifier=identifier, short_name=short_name, long_name=long_name,
                                                  manufacturer=manufacturer,
                                                  serial=serial, **kwargs)

        return qs

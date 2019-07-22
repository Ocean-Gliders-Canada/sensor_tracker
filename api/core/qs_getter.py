import re

from django.db.models import Q

from .util import (time_format_identifier,
                   INVALID_TIME_FORMAT,
                   YEAR_DAY,
                   YEAR_SEC,
                   time_to_time_range,
                   no_none_dict,
                   filter_objs)
from .exceptions import ImproperInput
from .decorator import query_optimize_decorator

from platforms.models import *
from instruments.models import *
from general.models import *

INCLUDE_ALL_SENSOR = 'ALL'


class GetQuerySetMethod:

    @staticmethod
    @query_optimize_decorator()
    def get_sensors_by_deployment(identifier=None, serial=None,
                                  platform_name=None, start_time=None, output=None):
        instrument_qs = GetQuerySetMethod.get_instruments(None, identifier=identifier,
                                                          serial=serial,
                                                          platform_name=platform_name,
                                                          start_time=start_time)
        instruments = list(instrument_qs)

        sensor_on_instrument_qs = SensorOnInstrument.objects.filter(instrument__in=instruments)
        sensor_pk_list = []
        for i in sensor_on_instrument_qs:
            sensor_pk_list.append(i.sensor_id)
        if output == INCLUDE_ALL_SENSOR.lower() or output == INCLUDE_ALL_SENSOR or not output:
            return Sensor.objects.filter(pk__in=sensor_pk_list)
        else:
            return Sensor.objects.filter(pk__in=sensor_pk_list, include_in_output=output)

    @staticmethod
    @query_optimize_decorator(['instrument'])
    def _get_sensors(identifier=None, standard_name=None, long_name=None, output=None):
        if not any([identifier, standard_name, long_name]):
            qs = Sensor.objects.all()
        else:
            the_dict = {
                "identifier": identifier,
                "short_name": standard_name,
                "long_name": long_name,
                "include_in_output": output
            }
            if output == INCLUDE_ALL_SENSOR.lower() or output == INCLUDE_ALL_SENSOR:
                the_dict.pop("include_in_output")
            the_dict = no_none_dict(the_dict)

            qs = Sensor.objects.filter(**the_dict)
        return qs

    @staticmethod
    def get_sensors(_, identifier=None, standard_name=None, long_name=None, platform_name=None, start_time=None,
                    instrument_identifier=None, instrument_serial=None,
                    output=None, **kwargs):
        if platform_name or instrument_identifier:
            return GetQuerySetMethod.get_sensors_by_deployment(identifier=instrument_identifier,
                                                               serial=instrument_serial, platform_name=platform_name,
                                                               start_time=start_time, output=output, **kwargs
                                                               )
        else:
            return GetQuerySetMethod._get_sensors(identifier=identifier, standard_name=standard_name,
                                                  long_name=long_name, output=output, **kwargs)

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
            platform_type_qs = GetQuerySetMethod.get_platform_type(model=model, how=how)
            platform_types = list(platform_type_qs)
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
            qs = None
            if start_time:
                time_format_type = time_format_identifier(start_time)
                # create for day range search when not providing full date detail
                if time_format_type == YEAR_DAY:
                    the_dict.pop("start_time")
                    begin, end = time_to_time_range(start_time)
                    qs = PlatformDeployment.objects.filter(start_time__gte=begin, start_time__lte=end)

            the_dict = no_none_dict(the_dict)
            if qs is None:
                qs = PlatformDeployment.objects.filter(**the_dict)
            else:
                qs = qs.filter(**the_dict)
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
    @query_optimize_decorator(['user', 'platform_deployment_comment_box'])
    def get_deployment_comment(platform_name=None, start_time=None):
        # query optimize problem
        if not any([platform_name, start_time]):
            qs = PlatformDeploymentComment.objects.all()
        else:
            deployment_qs = GetQuerySetMethod.get_deployment(None, platform_name=platform_name, start_time=start_time)
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
            pk_list.append(o.instrument_id)

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
            qs = Instrument.objects.filter(**the_dict)

        return qs

    @staticmethod
    @query_optimize_decorator()
    def get_instruments_by_deployment(platform_name=None, start_time=None):
        pk_list = []
        instrument_on_platform_qs = GetQuerySetMethod.get_instrument_on_platform_by_platform(
            platform_name=platform_name)
        if instrument_on_platform_qs:
            deployment_qs = GetQuerySetMethod.get_deployments(platform_name=platform_name, start_time=start_time)
            if deployment_qs:
                deployment_objs = list(deployment_qs)
                deployment_obj = deployment_objs[0]
                start_t = deployment_obj.start_time
                end_t = deployment_obj.end_time
                instrument_on_platform_qs.prefetch_related("instrument").filter(
                    Q(start_time__gte=start_t) & Q(end_time__lte=end_t) | Q(start_time__gte=start_t) & Q(
                        end_time=None))
                for o in instrument_on_platform_qs:
                    pk_list.append(o.instrument_id)
        return Instrument.objects.filter(pk__in=pk_list)

    @staticmethod
    def get_instruments(_, identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None,
                        platform_name=None, deployment_start_time=None, **kwargs):

        if platform_name:
            if deployment_start_time:
                qs = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                                     start_time=deployment_start_time,
                                                                     **kwargs)
            else:
                qs = GetQuerySetMethod.get_instrument_by_platform(platform_name=platform_name, **kwargs)
        else:
            # qs = GetQuerySetMethod.get_instrument(identifier=identifier, short_name=short_name, long_name=long_name,
            #                                       manufacturer=manufacturer,
            #                                       serial=serial, **kwargs)

            qs = Instrument.objects.all()
        return qs

    @staticmethod
    def get_instrument_comment(_, identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None,
                               platform_name=None, start_time=None, **kwargs):
        # todo: think about how to get comments
        ...

    @staticmethod
    @query_optimize_decorator(['platform', 'instrument'])
    def _get_instrument_on_platform(identifier=None):
        if identifier:
            qs = InstrumentOnPlatform.objects.filter(instrument__identifier=identifier)
        else:
            qs = InstrumentOnPlatform.objects.all()
        return qs

    @staticmethod
    @query_optimize_decorator(['platform', 'instrument'])
    def get_instrument_on_platform_by_platform(platform_name=None):

        instrument_on_platform_objs = InstrumentOnPlatform.objects.filter(platform__name=platform_name)

        return instrument_on_platform_objs

    @staticmethod
    def get_instrument_on_platform(_, identifier=None, platform_name=None, **kwargs):
        if platform_name:
            qs = GetQuerySetMethod.get_instrument_on_platform_by_platform(platform_name=platform_name, **kwargs)
        else:
            qs = GetQuerySetMethod._get_instrument_on_platform(identifier=identifier, **kwargs)
        return qs

    @staticmethod
    @query_optimize_decorator(["manufacturer"])
    def get_platform_type(model=None, how="match"):
        # ["match", "contains", "regex"]
        # all exceptions will be handled in upper level
        if model:

            try:
                lower_how = how.lower()
            except AttributeError:
                raise AttributeError("Invalid model")

            if lower_how == "match":
                qs = PlatformType.objects.filter(model=model)
            elif lower_how == 'contains':
                all_objs_query = PlatformType.objects.all()

                def filter_fun(obj):
                    try:
                        return (model.lower()) in obj.model.lower()
                    except AttributeError:
                        raise AttributeError("Invalid model")

                res_objs = filter_objs(all_objs_query,
                                       filter_fun
                                       )
                res_pk_list = []
                for o in res_objs:
                    res_pk_list.append(o.id)
                qs = PlatformType.objects.filter(pk__in=res_pk_list)
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

                res_objs = filter_objs(all_objs_query,
                                       filter_fun
                                       )
                res_pk_list = []
                for o in res_objs:
                    res_pk_list.append(o.id)
                qs = PlatformType.objects.filter(pk__in=res_pk_list)
            else:
                raise ImproperInput("how should be match or contains or regex")
        else:
            qs = PlatformType.objects.all()
        return qs

    @staticmethod
    @query_optimize_decorator(['user', 'platform_comment_box'])
    def get_platform_comment(platform_name=None):
        if platform_name:
            box_qs = PlatformCommentBox.objects.filter(platform__name=platform_name)
            box_pk_list = []
            for o in box_qs:
                box_pk_list.append(o.id)
            qs = PlatformComment.objects.filter(pk__in=box_pk_list)
        else:
            qs = PlatformComment.objects.all()
        return qs

    @staticmethod
    @query_optimize_decorator(['instrument', "sensor"])
    def get_sensor_on_instrument(platform_name=None, start_time=None):
        if any([platform_name, start_time]):
            instruments_qs = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                                             start_time=start_time)
            sensor_on_instrument_list = list(instruments_qs)
            qs = SensorOnInstrument.objects.filter(instrument__in=sensor_on_instrument_list)
        else:
            qs = SensorOnInstrument.objects.all()
        return qs

import re
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .util import (time_format_identifier,
                   YEAR_DAY,
                   time_to_time_range,
                   no_none_dict,
                   filter_objs)
from .exceptions import ImproperInput
from .decorator import query_optimize_decorator
from .util import change_to_case_insensitive_parameter
from platforms.models import *
from instruments.models import *
from general.models import *

INCLUDE_ALL_SENSOR = 'ALL'


class GetQuerySetMethod:

    @staticmethod
    @query_optimize_decorator()
    def get_sensors_by_deployment(identifier=None, serial=None,
                                  platform_name=None, deployment_start_time=None, output=None):
        instrument_qs = GetQuerySetMethod.get_instruments(None, identifier=identifier,
                                                          serial=serial,
                                                          platform_name=platform_name,
                                                          deployment_start_time=deployment_start_time)
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
            case_insensitive_parameter = change_to_case_insensitive_parameter(the_dict,
                                                                              ["identifier", "short_name", "long_name"])

            qs = Sensor.objects.filter(**case_insensitive_parameter)
        return qs

    @staticmethod
    def get_sensors(_, identifier=None, standard_name=None, long_name=None, platform_name=None,
                    deployment_start_time=None,
                    instrument_identifier=None, instrument_serial=None,
                    output=None, **kwargs):
        if platform_name or instrument_identifier:
            return GetQuerySetMethod.get_sensors_by_deployment(identifier=instrument_identifier,
                                                               serial=instrument_serial, platform_name=platform_name,
                                                               deployment_start_time=deployment_start_time,
                                                               output=output, **kwargs
                                                               )
        else:
            return GetQuerySetMethod._get_sensors(identifier=identifier, standard_name=standard_name,
                                                  long_name=long_name, output=output, **kwargs)

    @staticmethod
    @query_optimize_decorator(['platform_type', 'institution'])
    def get_platforms(platform_name=None, serial_number=None):
        # todo: Figure out why when depth = 0, there are some duplicated queries
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
            res = Manufacturer.objects.filter(name__iexact=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_institutions(name=None):
        if not name:
            return Institution.objects.all()
        else:
            res = Institution.objects.filter(name__iexact=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_project(name=None):
        if not name:
            return Project.objects.all()
        else:
            res = Project.objects.filter(name__iexact=name)
            return res

    @staticmethod
    @query_optimize_decorator()
    def get_power(name=None):
        if not name:
            qs = PlatformPowerType.objects.all()
        else:
            qs = PlatformPowerType.objects.filter(name__iexact=name)
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
        WMO_ID = "wmo_id"
        PLATFORM_NAME = "platform__name"
        INSTITUTION_NAME = "institution__name"
        PROJECT_NAME = "project__name"
        TITLE = "title"
        TESTING_MISSION = "testing_mission"
        START_TIME = "start_time"
        DEPLOYMENT_NUMBER = "deployment_number"

        the_dict = {
            WMO_ID: wmo_id,
            PLATFORM_NAME: platform_name,
            INSTITUTION_NAME: institution_name,
            PROJECT_NAME: project_name,
            TITLE: title,
            TESTING_MISSION: testing_mission,
            START_TIME: start_time,
            DEPLOYMENT_NUMBER: deployment_number
        }

        if not any(the_dict.values()):
            qs = PlatformDeployment.objects.all()
        else:
            qs = None
            if start_time:
                time_format_type = time_format_identifier(start_time)
                # create for day range search when not providing full date detail
                if time_format_type == YEAR_DAY:
                    the_dict.pop(START_TIME)
                    begin, end = time_to_time_range(start_time)
                    qs = PlatformDeployment.objects.filter(start_time__gte=begin, start_time__lte=end)

            the_dict = no_none_dict(the_dict)
            case_insensitive_dict_for_some_variables = change_to_case_insensitive_parameter(the_dict,
                                                                                            [PLATFORM_NAME,
                                                                                             INSTITUTION_NAME,
                                                                                             PROJECT_NAME])
            if qs is None:

                qs = PlatformDeployment.objects.filter(**case_insensitive_dict_for_some_variables)
            else:
                qs = qs.filter(**case_insensitive_dict_for_some_variables)
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
    def get_deployment_comment(platform_name=None, start_time=None, modified_date=None):
        # query optimize problem
        if not any([platform_name, start_time, modified_date]):
            qs = PlatformDeploymentComment.objects.all()
        else:
            if any([platform_name, start_time]):
                deployment_qs = GetQuerySetMethod.get_deployment(None, platform_name=platform_name,
                                                                 start_time=start_time)
                deployment_objs = list(deployment_qs)
                if deployment_objs:
                    deployment_obj = deployment_objs[0]
                    try:
                        deployment_comment_box = PlatformDeploymentCommentBox.objects.get(
                            platform_deployment=deployment_obj)
                    except ObjectDoesNotExist:
                        qs = PlatformDeploymentComment.objects.none()
                    else:
                        qs = PlatformDeploymentComment.objects.filter(
                            platform_deployment_comment_box=deployment_comment_box)
                        if modified_date:
                            qs.filter(modified_date__gt=modified_date)
                else:
                    qs = PlatformDeploymentComment.objects.none()

            elif modified_date:
                qs = PlatformDeploymentComment.objects.filter(modified_date__gt=modified_date)
            else:
                qs = PlatformDeploymentComment.objects.none()
        return qs

    @staticmethod
    @query_optimize_decorator(['manufacturer'])
    def get_instrument_by_platform(platform_name=None):
        if platform_name:
            qs = InstrumentOnPlatform.objects.filter(platform__name__iexact=platform_name).prefetch_related(
                'instrument')
            instrument_on_platform_objs = list(qs)
            pk_list = []
            for o in instrument_on_platform_objs:
                pk_list.append(o.instrument_id)

            qs = Instrument.objects.filter(pk__in=pk_list)
        else:
            qs = Instrument.objects.all()

        return qs

    @staticmethod
    @query_optimize_decorator(['manufacturer'])
    def get_instrument(identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None):
        if not (identifier or short_name or long_name or serial or manufacturer):
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
            case_insensitive_parameter = change_to_case_insensitive_parameter(the_dict,
                                                                              ["identifier", "short_name", "long_name",
                                                                               "manufacturer__name"])
            qs = Instrument.objects.filter(**case_insensitive_parameter)

        return qs

    @staticmethod
    @query_optimize_decorator(['instrument'])
    def get_instruments_by_deployment(platform_name=None, deployment_start_time=None):
        pk_list = []
        if deployment_start_time:

            instrument_on_platform_qs = GetQuerySetMethod.get_instrument_on_platform_by_platform(
                platform_name=platform_name)
            if instrument_on_platform_qs:

                deployment_qs = GetQuerySetMethod.get_deployments(platform_name=platform_name,
                                                                  start_time=deployment_start_time)
                if deployment_qs:
                    deployment_objs = list(deployment_qs)
                    for deployment_obj in deployment_objs:
                        start_t = deployment_obj.start_time
                        end_t = deployment_obj.end_time
                        if end_t:
                            instrument_on_platform_qs = instrument_on_platform_qs.filter(
                                Q(start_time__lte=start_t) & Q(end_time__gte=end_t) | Q(start_time__lte=start_t) & Q(
                                    end_time=None))
                        else:
                            instrument_on_platform_qs = instrument_on_platform_qs.filter(
                                Q(start_time__lte=start_t))
                        for o in instrument_on_platform_qs:
                            if o.end_time:
                                if o.end_time > start_t:
                                    the_id = o.instrument_id
                                    if the_id not in pk_list:
                                        pk_list.append(the_id)
                            else:
                                the_id = o.instrument_id
                                if the_id not in pk_list:
                                    pk_list.append(the_id)
            return Instrument.objects.filter(pk__in=pk_list)
        else:
            return GetQuerySetMethod.get_instrument_by_platform(platform_name=platform_name)

    @staticmethod
    def get_instruments(_, identifier=None, short_name=None, long_name=None, manufacturer=None, serial=None,
                        platform_name=None, deployment_start_time=None, **kwargs):

        if platform_name:
            if deployment_start_time:
                qs = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                                     deployment_start_time=deployment_start_time,
                                                                     **kwargs)
            else:
                qs = GetQuerySetMethod.get_instrument_by_platform(platform_name=platform_name, **kwargs)
        else:
            qs = GetQuerySetMethod.get_instrument(identifier=identifier, short_name=short_name, long_name=long_name,
                                                  manufacturer=manufacturer,
                                                  serial=serial, **kwargs)
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
            qs = InstrumentOnPlatform.objects.filter(instrument__identifier__iexact=identifier)
        else:
            qs = InstrumentOnPlatform.objects.all()
        return qs

    @staticmethod
    @query_optimize_decorator(['platform', 'instrument'])
    def get_instrument_on_platform_by_platform(platform_name=None):
        if platform_name:
            instrument_on_platform_objs = InstrumentOnPlatform.objects.filter(platform__name__iexact=platform_name)
        else:
            instrument_on_platform_objs = InstrumentOnPlatform.objects.all()

        return instrument_on_platform_objs

    @staticmethod
    @query_optimize_decorator(['platform', 'instrument'])
    def get_instrument_on_platform_by_platform_and_time(platform_name, start_time=None, end_time=None):
        instrument_on_platform_objs = InstrumentOnPlatform.objects.filter(platform__name=platform_name)
        if end_time:
            instrument_on_platform_objs = instrument_on_platform_objs.filter(
                Q(start_time__lte=start_time) & Q(end_time__gte=end_time) | Q(start_time__lte=start_time) & Q(
                    end_time=None))
        else:
            instrument_on_platform_objs = instrument_on_platform_objs.filter(Q(start_time__lte=start_time))

        instrument_on_platform_objs = instrument_on_platform_objs.order_by('instrument_id')
        return instrument_on_platform_objs

    @staticmethod
    def get_instrument_on_platform(_, identifier=None, platform_name=None, **kwargs):
        if platform_name:
            qs = GetQuerySetMethod.get_instrument_on_platform_by_platform(platform_name=platform_name, **kwargs)
        else:
            qs = GetQuerySetMethod._get_instrument_on_platform(identifier=identifier, **kwargs)
        return qs

    @staticmethod
    def get_instrument_on_platform_by_instrument(identifier=None, serial=None):
        qs = InstrumentOnPlatform.objects.all()
        if identifier:
            qs = qs.filter(instrument__identifier__iexact=identifier)
        if serial:
            qs = qs.filter(instrument__serial=serial)
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
                qs = PlatformType.objects.filter(model__iexact=model)
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
            box_qs = PlatformCommentBox.objects.filter(platform__name__iexact=platform_name)
            box_pk_list = []
            for o in box_qs:
                box_pk_list.append(o.id)
            qs = PlatformComment.objects.filter(pk__in=box_pk_list)
        else:
            qs = PlatformComment.objects.all()
        return qs

    @staticmethod
    @query_optimize_decorator(['instrument', "sensor"])
    def get_sensor_on_instrument(platform_name=None, deployment_start_time=None, instrument_identifier=None):
        if any([platform_name, deployment_start_time, instrument_identifier]):
            instruments_qs = None
            if any([platform_name, deployment_start_time]):
                instruments_qs = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                                                 deployment_start_time=deployment_start_time)

            if instruments_qs is None:
                if instrument_identifier:
                    instruments_qs = Instrument.objects.filter(identifier__iexact=instrument_identifier)
                else:
                    instruments_qs = SensorOnInstrument.objects.none()
            else:
                if instrument_identifier:
                    instruments_qs = instruments_qs.filter(identifier__iexact=instrument_identifier)

            sensor_on_instrument_list = list(instruments_qs)
            qs = SensorOnInstrument.objects.filter(instrument__in=sensor_on_instrument_list)
        else:
            qs = SensorOnInstrument.objects.all()
        return qs

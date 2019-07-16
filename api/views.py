# -*- coding: utf-8 -*-
import copy
import json
import datetime

from api.specs import specs
from api.core.qs_getter import (
    # get_instrument_by_platform,
    # get_instruments_by_deployment,
    # get_platform_type,
    get_deployment_by_platform_name_start_time,
    get_sensors_by_deployment,
    get_deployments_by_platform,
    get_sensors_by_platform as get_sensor_b_platform,

)
from api.core.receiver import receiver
from api.core.exceptions import VariableError
from api.api_base import ApiBaseView

from django.apps import apps
from django.http import HttpResponse
from django.template import loader
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from api import specs
from api.core import serializer
from api.core.qs_getter import GetQuerySetMethod
from rest_framework.authtoken import views as r_views

# General Models

class GetManufacturer(ApiBaseView):
    accept_option = {
        "name": "The name of manufactures"
    }
    serializer_class = serializer.ManufacturerSerializer
    queryset_method = GetQuerySetMethod.get_manufacturer


class GetInstitutions(ApiBaseView):
    accept_option = {
        "name": "The name of the institution."
    }
    queryset_method = GetQuerySetMethod.get_institutions
    serializer_class = serializer.InstitutionSerializer


class GetProject(ApiBaseView):
    accept_option = {
        "name": "The name of the project."
    }
    queryset_method = GetQuerySetMethod.get_project
    serializer_class = serializer.ProjectSerializer


# Instrument models
class GetInstrument(ApiBaseView):
    accept_option = {
        "identifier": "The name used to identify this instrument in the raw data.",
        "short_name": "The short, general name for the instrument.",
        "long_name": "The full name for the instrument",
        "serial": "Serial number of instrument",
        "manufacturer": "",
        "platform_name": "",
        "start_time": ""
    }
    mutual_exclusion = (
        ["identifier", "short_name", "long_name", "serial", "manufacturer"], ["platform_name", "start_time"])
    variable_error_message = 'No variable accept'
    serializer_class = serializer.InstrumentSerializer
    queryset_method = GetQuerySetMethod.get_instruments


class GetSensor(ApiBaseView):
    accept_option = [
        "identifier",
        "short_name",
        "long_name",
        "platform_name",
        "start_time"
    ]
    mutual_exclusion = (
        ["identifier",
         "short_name",
         "long_name"], ["platform_name", "start_time"])
    serializer_class = serializer.SensorSerializer
    queryset_method = GetQuerySetMethod.get_sensors


# todo : think about how ppl would use this
# class GetInstrumentComment(ApiBaseView):
#     accept_option = [
#         "identifier",
#         "short_name",
#         "long_name",
#         "platform_name",
#         "start_time"
#     ]
#     mutual_exclusion = (
#         ["identifier",
#          "short_name",
#          "long_name"], ["platform_name", "start_time"])
#     serializer_class = serializer.InstrumentCommentSerializer
#     queryset_method = GetQuerySetMethod.get_sensors

class GetInstrumentOnPlatform(ApiBaseView):
    accept_option = [
        "identifier",
        "platform_name"
    ]
    mutual_exclusion = (
        "identifier",
        "platform_name")
    serializer_class = serializer.InstrumentOnPlatformSerializer
    queryset_method = GetQuerySetMethod.get_instrument_on_platform


# platform model
class GetPower(ApiBaseView):
    accept_option = {
        "name": "The name of the battery."
    }
    serializer_class = serializer.PlatformPowerTypeSerializer
    queryset_method = GetQuerySetMethod.get_power


class GetPlatform(ApiBaseView):
    accept_option = {
        "platform_name": "The name used to identify this instrument in the raw data.",
        "serial_name": "",
        "model": "",
        "how": ""
    }
    mutual_exclusion = (
        ["platform_name", "serial_name"], ["model", "how"])
    serializer_class = serializer.PlatformSerializer
    queryset_method = GetQuerySetMethod.get_platform


class GetPlatformType(ApiBaseView):
    accept_option = ["model", "how"]
    serializer_class = serializer.PlatformTypeSerializer
    queryset_method = GetQuerySetMethod.get_platform_type


class GetDeployment(ApiBaseView):
    accept_option = [
        "wmo_id", "platform_name", "institution_name", "project_name", "testing_mission", "start_time",
        "deployment_number", "model", "how"
    ]
    mutual_exclusion = (
        ["wmo_id", "platform_name", "institution_name", "project_name", "testing_mission", "start_time",
         "deployment_number"], ["model", "how"])
    serializer_class = serializer.PlatformDeploymentSerializer
    queryset_method = GetQuerySetMethod.get_deployment


class GetPlatformDeploymentComment(ApiBaseView):
    accept_option = {
        "platform": "The name of deployment's platform",
        "start_time": "The start time of deployment"
    }
    serializer_class = serializer.PlatformDeploymentCommentSerializer
    queryset_method = GetQuerySetMethod.get_deployment_comment


class GetPlatformComment(ApiBaseView):
    accept_option = {
        "platform": "The name of deployment's platform",
    }
    serializer_class = serializer.PlatformCommentSerializer
    queryset_method = GetQuerySetMethod.get_platform_comment


# special Apis


class GetPlatformDeployments(ApiBaseView):
    accept = {
        "platform_name": "The name of deployment's platform",
        "start_time": "The start time of deployment"
    }

    @classmethod
    @api_view(['GET'])
    @receiver
    def get_platform_deployments(cls, request):
        return cls.api_get(request, get_deployments_by_platform)


class GetSensorsByPlatform(ApiBaseView):
    accept = {
        "platform_name": "The name of deployment's platform",
    }

    @classmethod
    @api_view(['GET'])
    @receiver
    def get_sensors_by_platform(cls, request):
        return cls.api_get(request, get_sensor_b_platform)


class GetSensorByDeployment(ApiBaseView):
    accept = {
        "platform_name": "The name of deployment's platform",
        "start_time": "The start time of deployment"
    }

    @classmethod
    @api_view(['GET'])
    @receiver
    def get_sensors_by_deployment(cls, request):
        the_get = copy.deepcopy(request.GET)
        return cls.api_get(the_get, get_sensors_by_deployment)


class GetDeploymentByPlatformNameStartTime(ApiBaseView):
    accept = {
        "platform_name": "The name of deployment's platform",
        "start_time": "The start time of deployment"
    }

    @classmethod
    @api_view(['GET'])
    @receiver
    def get_deployment_by_platform_name_start_time(cls, request):
        return cls.api_get(request, get_deployment_by_platform_name_start_time)


class GetAllDeployments(ApiBaseView):
    accept = {
        "platform_name": "The name of deployment's platform",
    }
    summary = "Return all the deployment"
    variable_error_message = 'No variable accept'

    @classmethod
    @api_view(['GET'])
    @receiver
    def get_all_deployments(cls, request):
        return cls.api_get(request, get_instrument_by_platform)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication, SessionAuthentication])
# def get_token(request):
#     ...

#
# class GetInstrument(ApiBase):
#     accept_option = {
#         "identifier": "The name used to identify this instrument in the raw data.",
#         "short_name": "The short, general name for the instrument.",
#         "long_name": "The full name for the instrument",
#         "serial": "Serial number of instrument"
#     }
#     variable_error_message = 'No variable accept'
#
#     @classmethod
#     @api_view(['GET'])
#     @receiver
#     def get_instruments(cls, request):
#         return cls.api_get(request, g_instruments)


# POST Requests


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_deployment(request):
    Deployment = apps.get_model('platforms', 'PlatformDeployment')
    types = {"wmo_id": int, "deployment_number": int, "platform_id": int, "institution_id": int, "project_id": int,
             "power_type_id": int, "platform_name": str, "title": str, "start_time": str, "end_time": str,
             "testing_mission": bool, "comment": str, "acknowledgement": str,
             "contributor_name": str, "contributor_role": str, "creator_email": str, "creator_name": str,
             "creator_url": str, "data_repository_link": str, "publisher_email": str, "publisher_name": str,
             "publisher_url": str, "metadata_link": str, "references": str, "sea_name": str,
             "latitude": float, "longitude": float, "depth": float}
    deployment = create_object_from_request(request, Deployment, value_type=types)

    return save_and_result(deployment)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_platform(request):
    Platform = apps.get_model('platforms', 'Platform')
    platform = create_object_from_request(request, Platform)

    return save_and_result(platform)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_project(request):
    Project = apps.get_model('general', 'Project')
    project = create_object_from_request(request, Project)

    return save_and_result(project)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_instrument_on_platform(request):
    InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')
    instrument_on_platform = create_object_from_request(request, InstrumentOnPlatform)

    return save_and_result(instrument_on_platform)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_platform_type(request):
    PlatformType = apps.get_model('platforms', 'PlatformType')
    platform_type = create_object_from_request(request, PlatformType)

    return save_and_result(platform_type)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_instrument(request):
    Instrument = apps.get_model('instruments', 'Instrument')
    instrument = create_object_from_request(request, Instrument)

    return save_and_result(instrument)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_sensor(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    sensor = create_object_from_request(request, Sensor)

    return save_and_result(sensor)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_component(request):
    lookup = {
        'deployment': ('platforms', 'PlatformDeployment'),
        'platform': ('platforms', 'Platform'),
        'project': ('general', 'Project'),
        'instruments_platform': ('instruments', 'InstrumentOnPlatform'),
        'platform_type': ('platforms', 'PlatformType'),
        'instrument': ('instruments', 'Instrument'),
        'sensor': ('instruments', 'Sensor'),
    }
    if 'component' in request.POST and 'id' in request.POST:
        try:
            Component = apps.get_model(*lookup[request.POST.get('component')])
        except KeyError:
            err = "'%s' is not a component." % request.POST.get('component')
            return error_result(err)

        try:
            component = Component.objects.filter(id=request.POST.get('id'))
            if len(component) == 0:
                err = 'Could not find %s with that id.' % request.POST.get('component')
                return error_result(err)
            component = component.first()
        except ValueError:
            err = "'id' must be an integer."
            return error_result(err)
        fields = [x.get_attname_column()[0] for x in Component._meta.fields]
        fields.remove('id')
        for field in fields:
            if field in request.POST:
                setattr(component, field, request.POST.get(field))
        component.save()
        res = {
            'success': True,
            'message': 'Updated \'%s\' with id %s.' % (
                request.POST.get('component'),
                request.POST.get('id')
            )
        }
        return HttpResponse(json.dumps(res), content_type='application/json')


def spec(request):
    template = loader.get_template('spec.html')
    context = {
        'urls': specs.specs,
        'links': specs.links
    }
    return HttpResponse(template.render(context, request))


# Helpers
def create_object_from_request(request, object, time_columns=None, value_type=None):
    if time_columns is None:
        time_columns = ['start_time', 'end_time']
    fields = [x.get_attname_column()[0] for x in object._meta.fields]
    kargs = {}
    for field in fields:
        if field in request.POST:
            if field in time_columns:
                kargs[field] = datetime.datetime.strptime(request.POST.get(field), '%Y-%m-%d %H:%M:%S')
            else:
                kargs[field] = request.POST.get(field)
    if value_type is not None:
        kargs = check_input_type(kargs, value_type)
    return object(**kargs)


def check_input_type(content, value_type):
    new_content = {}
    for key in content:
        value = content[key]
        if key in value_type:
            t = value_type[key]
            try:
                new_item = t(value)
            except:
                new_item = None
            new_content[key] = new_item
    return new_content


def save_and_result(model):
    try:
        model.save()
        res = {
            'success': True,
            'id': model.id
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    except Exception as e:
        print(e)
        return error_result(e.message.replace('DETAIL', '').strip())


def error_result(error):
    res = {'success': False, 'error': error}
    return HttpResponse(json.dumps(res), content_type='application/json')


def convert_times(obj):
    if type(obj) == dict:
        for k in obj:
            if type(obj[k]) == datetime.datetime:
                obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')


def clean_model_dict(models, no_foreign=['wmo_id']):
    data = []
    for m in models:
        m_dict = copy.deepcopy(m.__dict__)
        del m_dict['_state']
        keys = m_dict.keys()
        to_add = []
        for key in keys:
            if 'id' in key and key not in no_foreign:
                if key != 'id':
                    to_add.append(key.replace('_id', ''))
        for add in to_add:
            try:
                m_dict[add] = copy.deepcopy(getattr(m, add).__dict__)
                convert_times(m_dict[add])
                del m_dict[add]['_state']
            except AttributeError:
                pass  # It's a false alarm
        convert_times(m_dict)
        data.append(m_dict)
    return data


def format_time(t):
    return datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')




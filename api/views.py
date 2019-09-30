# -*- coding: utf-8 -*-

from collections import OrderedDict

from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse

from django.urls import NoReverseMatch

from .core.api_base import ApiBaseView
from .core import serializer
from .core.qs_getter import GetQuerySetMethod


# General Models

class GetManufacturer(ApiBaseView):
    """Get manufacturer data"""
    accept_basic = {
        "name": "The name of manufactures",
    }
    serializer_class = serializer.ManufacturerSerializer
    queryset_method = GetQuerySetMethod.get_manufacturer


class GetInstitutions(ApiBaseView):
    """Get institution data"""
    accept_basic = {
        "name": "The name of the institution."
    }
    queryset_method = GetQuerySetMethod.get_institutions
    serializer_class = serializer.InstitutionSerializer


class GetProject(ApiBaseView):
    """Get project data"""
    accept_basic = {
        "name": "The name of the project."
    }
    queryset_method = GetQuerySetMethod.get_project
    serializer_class = serializer.ProjectSerializer


# Instrument models
class GetInstrument(ApiBaseView):
    """Get instrument data list"""
    accept_basic = {"identifier": "The name used to identify this instrument in the raw data.",
                    "short_name": "The short, general name for the instrument.",
                    "long_name": "The full name for the instrument",
                    "serial": "The serial number of Instrument"}

    accept_option = {
        "platform_name": "The name of platform that the instrument attach to",
        "deployment_start_time": "The start time of the deployment"
    }
    mutual_exclusion = (
        ["identifier", "short_name", "long_name", "serial"], ["platform_name", "start_time"])
    variable_error_message = 'No variable accept'
    serializer_class = serializer.InstrumentSerializer
    queryset_method = GetQuerySetMethod.get_instruments


class GetSensor(ApiBaseView):
    """Get sensor data"""
    accept_basic = {
        "identifier": "The identifier of the sensor",
        "short_name": "The short name of the sensor",
        "long_name": "The long name of the sensor",
    }
    accept_option = {
        "platform_name": "The name of the platform with sensor attach to",
        "deployment_start_time": "The start time of deployment",
        "instrument_identifier": "The name of the instrument that sensor attach to",
        "instrument_serial": "The serial number of the instrument that sensor attach to",
        "output": "if the include in output option checked"
    }
    mutual_exclusion = (
        ["identifier", "short_name", "long_name"],
        ["platform_name", "deployment_start_time"],
        ["instrument_identifier", "instrument_serial"])
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


class GetSensorOnInstrument(ApiBaseView):
    """Get sensor on instrument data"""
    accept_option = {
        "platform_name": "The name of the platform",
        "deployment_start_time": "The start time of the deployment",
        "instrument_identifier": "The identifier of instrument"
    }
    serializer_class = serializer.SensorOnInstrumentSerializer
    queryset_method = GetQuerySetMethod.get_sensor_on_instrument


class GetInstrumentOnPlatform(ApiBaseView):
    """Get instrument on platform data"""
    accept_option = {
        "identifier": "The identifier of the instrument",
        "platform_name": "The name of the platform"
    }
    mutual_exclusion = (
        "identifier",
        "platform_name")
    serializer_class = serializer.InstrumentOnPlatformSerializer
    queryset_method = GetQuerySetMethod.get_instrument_on_platform


# platform model
class GetPower(ApiBaseView):
    """Get power data"""
    accept_basic = {
        "name": "The name of the battery."
    }
    serializer_class = serializer.PlatformPowerTypeSerializer
    queryset_method = GetQuerySetMethod.get_power


class GetPlatform(ApiBaseView):
    """Get platform data"""
    accept_basic = {
        "name": "The name used to identify this instrument in the raw data.",
        "serial_number": "The serial number of the platform",
        "active": "",
        "wmo_id": "",
    }
    accept_option = {
        "model": "The model of the platform",
        "how": "The way how to filter the platform"
    }
    mutual_exclusion = (
        ["platform_name", "serial_number", "active", "wmo_id"],
        ["model", "how"])
    serializer_class = serializer.PlatformSerializer
    queryset_method = GetQuerySetMethod.get_platform


class GetPlatformType(ApiBaseView):
    """Get platform type data"""
    accept_option = {
        "model": "The model of the ",
        "how": "The way how to filter out the platform model"
    }
    serializer_class = serializer.PlatformTypeSerializer
    queryset_method = GetQuerySetMethod.get_platform_type


class GetDeployment(ApiBaseView):
    """Get deployment data"""
    accept_basic = {
        "wmo_id": "The WMO ID of the deployment",
        "testing_mission": "The name of the testing mission",
        "deployment_number": "The deployment number of the mission",
        "sea_name": "",
    }
    accept_option = {
        "start_time": "The start time of the deployment",
        "platform_name": "The name of the platform",
        "institution_name": "The name of institution",
        "model": "The model of the platform",
        "how": "The way how to filter the platform"
    }
    mutual_exclusion = (
        ["wmo_id", "platform_name", "institution_name", "project_name", "testing_mission", "start_time",
         "deployment_number", "sea_name"],
        ["model", "how"])
    serializer_class = serializer.PlatformDeploymentSerializer
    queryset_method = GetQuerySetMethod.get_deployment


class GetPlatformDeploymentComment(ApiBaseView):
    """Get platform deployment data"""
    accept_option = {
        "platform_name": "The name of deployment's platform",
        "start_time": "The start time of deployment",
        "modified_date": "The time of comment modified"
    }
    serializer_class = serializer.PlatformDeploymentCommentSerializer
    queryset_method = GetQuerySetMethod.get_deployment_comment


class GetPlatformComment(ApiBaseView):
    """Get platform comment data"""
    accept_option = {
        "platform_name": "The name of deployment's platform",
    }
    serializer_class = serializer.PlatformCommentSerializer
    queryset_method = GetQuerySetMethod.get_platform_comment


class APIRootView(views.APIView):
    """
    The default basic root view for DefaultRouter
    """
    _ignore_model_permissions = True
    schema = None  # exclude from schema
    api_root_dict = None

    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

        the_request = request._request
        ret["swagger"] = the_request._current_scheme_host + the_request.path + "swagger/"
        ret["redoc"] = the_request._current_scheme_host + the_request.path + "redoc/"
        ret["sensor_tracker_api_library"] = "https://gitlab.oceantrack.org/ceotr/metadata-tracker/tracker_api"
        ret.move_to_end("sensor_tracker_api_library", last=False)
        ret.move_to_end("redoc", last=False)
        ret.move_to_end("swagger", last=False)
        return Response(ret)

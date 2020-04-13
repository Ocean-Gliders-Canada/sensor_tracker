from api.core.qs_getter import GetQuerySetMethod
import json
import datetime
from platforms.models import *
from instruments.models import *
from general.models import *


class GetHierarchy:

    GET_FDEPLOYMENT_FUNCTION = GetQuerySetMethod.get_deployments
    GET_INSTRUMENT_FUNCTION = GetQuerySetMethod.get_instrument_on_platform_by_platform_and_time
    GET_SENSOR_FUNCTION = GetQuerySetMethod.get_sensor_on_instrument

    def get_sensors_list(self, sensors, sensor_fields):
        sensor_list = []
        for sensor in sensors:
            sensor_dict = {}
            for sen_field in sensor_fields:
                value = getattr(sensor, sen_field)
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, (PlatformType, Institution, Manufacturer, Instrument)):
                    value = str(value)
                sensor_dict[sen_field] = value
            sensor_list.append(sensor_dict)
        return sensor_list

    def get_instrument_list(self, sensor_qs, sensor_fields, instrument_qs, instrument_fields):
        instrument_list = []
        for ins in instrument_qs:
            instrument_dict = {}
            for ins_field in instrument_fields:
                value = getattr(ins, ins_field)
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, (PlatformType, Institution, Manufacturer, Instrument)):
                    value = str(value)
                instrument_dict[ins_field] = value
            sensors = sensor_qs.pop(0)
            sensor_list = self.get_sensors_list(sensors, sensor_fields)
            instrument_dict['sensors_on_curr_instrument'] = sensor_list
            instrument_list.append(instrument_dict)
        return instrument_list

    def _get_json(self, sensor_qs, instrument_qs, platform_obj):
        res = {}
        platform = Platform._meta.fields
        platform_fields = [platform[i].name for i in range(len(platform))]
        for plat_field in platform_fields:
            value = getattr(platform_obj, plat_field)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, (PlatformType, Institution, Manufacturer, Instrument)):
                value = str(value)
            res[plat_field] = value
        sensor = Sensor._meta.fields
        sensor_fields = [sensor[i].name for i in range(len(sensor))]
        instrument = Instrument._meta.fields
        instrument_fields = [instrument[i].name for i in range(len(instrument))]
        instrument_list = self.get_instrument_list(sensor_qs, sensor_fields, instrument_qs, instrument_fields)
        res['instrument_on_curr_platform'] = instrument_list
        json_res = json.dumps(res)
        return json_res

    def get_sensor_qs(self, sensor_on_instrument_qs):
        sensor_qs = []
        for sensor_on_instrument_list in sensor_on_instrument_qs:
            print(sensor_on_instrument_list)
            sensors = []
            for sensor_on_instrument in sensor_on_instrument_list:
                sensors.append(sensor_on_instrument.sensor)
            sensor_qs.append(sensors)
        return sensor_qs

    def get_sensor_and_instrument_qs(self, instrument_on_platform_qs):
        instrument_qs = []
        sensor_on_instrument_qs = []
        for ins in instrument_on_platform_qs:
            sensors = self.GET_SENSOR_FUNCTION(instrument_identifier=ins.instrument.identifier)
            sensor_on_instrument_qs.append(sensors)
            instrument_qs.append(ins.instrument)
        return instrument_qs, sensor_on_instrument_qs

    def get_hierarchy_by_platform_name(self, platform_name, start_time):
        platform_development_obj_qs = self.GET_FDEPLOYMENT_FUNCTION(platform_name=platform_name, start_time=start_time)
        if platform_development_obj_qs:
            platform_development_obj = platform_development_obj_qs[0]
        else:
            return json.dumps({})
        start_time = platform_development_obj.start_time
        end_time = platform_development_obj.end_time
        platform_obj = platform_development_obj.platform
        platform_name = platform_development_obj.platform.name
        instrument_on_platform_qs = self.GET_INSTRUMENT_FUNCTION(
            platform_name=platform_name, start_time=start_time, end_time=end_time).prefetch_related(
            'platform').prefetch_related('instrument')
        instrument_qs, sensor_on_instrument_qs = self.get_sensor_and_instrument_qs(instrument_on_platform_qs)
        sensor_qs = self.get_sensor_qs(sensor_on_instrument_qs)
        json_res = self._get_json(sensor_qs, instrument_qs, platform_obj)
        return json_res


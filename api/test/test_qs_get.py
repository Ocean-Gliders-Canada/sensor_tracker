from django.test import TestCase

from rest_framework.test import APIRequestFactory

from .create_mock_sensor_tracker_database import create_mock_database, replace_to_id
from general import models as general
from instruments import models as instruments
from platforms import models as platforms
from app_common.utilities.time_format_functions import *

from api.core.qs_getter import GetQuerySetMethod


class QsGetTest(TestCase):
    def setUp(self):
        self.database_json = create_mock_database()
        self.instrument_on_platform_dict_data = self.database_json["instrument_on_platform"]
        self.platform_dict_data = self.database_json["platform"]

    def test_get_instrument_by_platform_all(self):
        # If not given the platform name or start time, it should return all the instrument has attached on platform
        instrument_on_platform_dict_data = self.database_json["instrument_on_platform"]
        res = GetQuerySetMethod.get_instruments_by_deployment()
        expected_instrument_ids = []
        for x in instrument_on_platform_dict_data:
            if x["instrument_id"] not in expected_instrument_ids:
                expected_instrument_ids.append(x["instrument_id"])
        ret_ids = []
        for obj in res:
            id = obj.id
            if id not in ret_ids:
                ret_ids.append(id)
        self.assertEqual(sorted(ret_ids), sorted(expected_instrument_ids))

    def test_get_instrument_by_platform_platform_namd_start_time(self):
        platform_name = "scotia"
        deployment_start_time = "2019-09-25"
        deployment_start_time_datetime = str_to_timeobj(deployment_start_time, '%Y-%m-%d')
        deployment_end_time_datetime = None
        # if given platform name and start_time, it should return all instrument which is activate at that range

        res = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                              deployment_start_time=deployment_start_time)

        the_platform_id = None
        for x in self.platform_dict_data:
            if x["name"] == platform_name:
                the_platform_id = x["id"]

        expected_instrument_ids = []
        for the_dict in self.instrument_on_platform_dict_data:
            platform_id = the_dict["platform_id"]
            start_time_str = the_dict["start_time"]
            end_time_str = the_dict["end_time"]
            start_time_str_obj = str_to_timeobj(start_time_str, time_format='%Y-%m-%dT%H:%M:%SZ')
            if end_time_str:
                try:
                    end_time_str_obj = str_to_timeobj(end_time_str, time_format='%Y-%m-%dT%H:%M:%SZ')
                except Exception:
                    end_time_str_obj = str_to_timeobj(end_time_str, time_format='%Y-%m-%dT%H:%M:%S.%fZ')
            else:
                end_time_str_obj = None

            if platform_id == the_platform_id:
                the_id = the_dict["instrument_id"]
                if the_id not in expected_instrument_ids:
                    if not deployment_end_time_datetime:
                        if start_time_str_obj <= deployment_start_time_datetime:
                            if not end_time_str_obj or deployment_start_time_datetime <= end_time_str_obj:
                                expected_instrument_ids.append(the_dict["instrument_id"])
                        else:
                            expected_instrument_ids.append(the_dict["instrument_id"])

        ret_ids = []
        for obj in res:
            id = obj.id
            if id not in ret_ids:
                ret_ids.append(id)
        self.assertEqual(sorted(ret_ids), sorted(expected_instrument_ids))

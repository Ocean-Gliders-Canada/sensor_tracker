from django.test import TestCase

from .create_mock_sensor_tracker_database import create_mock_database
from app_common.utilities.time_format_functions import *

from api.core.qs_getter import GetQuerySetMethod


def get_platform_id(platform_dict, platform_name):
    the_platform_id = None
    for x in platform_dict:
        if x["name"] == platform_name:
            the_platform_id = x["id"]
    return the_platform_id


def time_str_to_time_obj(time_str):
    if time_str:
        try:
            time_obj = str_to_timeobj(time_str, time_format='%Y-%m-%d')
            return time_obj
        except ValueError:
            try:
                time_obj = str_to_timeobj(time_str, time_format='%Y-%m-%dT%H:%M:%SZ')
                return time_obj
            except ValueError:
                time_obj = str_to_timeobj(time_str, time_format='%Y-%m-%dT%H:%M:%S.%fZ')
                return time_obj
    return None


def common_time_period(start_time1, end_time1, start_time2, end_time2):
    if end_time1 is not None and end_time2 is not None:
        if end_time1 <= start_time1:
            return False
        elif end_time2 <= start_time1:
            return False
        else:
            return True
    elif end_time1 is None and end_time2 is not None:
        if start_time1 >= end_time2:
            return False
    elif end_time1 is not None and end_time2 is None:
        if start_time2 >= end_time1:
            return False
    return True


def get_objs_or_qs_ids_sorted(qs_or_objs):
    ret_ids = []
    for obj in qs_or_objs:
        id = obj.id
        if id not in ret_ids:
            ret_ids.append(id)
    return sorted(ret_ids)


class QsGetTest(TestCase):
    def setUp(self):
        self.database_json = create_mock_database()
        self.instrument_on_platform_dict_data = self.database_json["instrument_on_platform"]
        self.platform_dict_data = self.database_json["platform"]

    def test_get_instrument_by_platform_platform_namd_start_time_no_end_time(self):
        platform_name = "scotia"
        deployment_start_time = "2019-09-25"
        deployment_start_time_datetime = time_str_to_time_obj(deployment_start_time)
        deployment_end_time_datetime = None
        # if given platform name and start_time, it should return all instrument which is activate at that range

        res = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                              deployment_start_time=deployment_start_time)

        the_platform_id = get_platform_id(self.platform_dict_data, platform_name)

        expected_instrument_ids = []
        for the_dict in self.instrument_on_platform_dict_data:
            platform_id = the_dict["platform_id"]
            start_time_str = the_dict["start_time"]
            end_time_str = the_dict["end_time"]
            start_time_str_obj = time_str_to_time_obj(start_time_str)
            if end_time_str:
                end_time_str_obj = time_str_to_time_obj(end_time_str)

            else:
                end_time_str_obj = None

            if platform_id == the_platform_id:
                the_id = the_dict["instrument_id"]
                if the_id not in expected_instrument_ids:
                    if common_time_period(start_time_str_obj, end_time_str_obj, deployment_start_time_datetime,
                                          deployment_end_time_datetime):
                        expected_instrument_ids.append(the_dict["instrument_id"])

        self.assertEqual(get_objs_or_qs_ids_sorted(res), sorted(expected_instrument_ids))

    def test_get_instrument_by_deployment_platform_name_and_start_time_with_end_time(self):
        platform_name = "scotia"
        deployment_start_time = "2019-9-26"
        deployment_start_time_datetime = time_str_to_time_obj(deployment_start_time)
        deployment_end_time_datetime = None
        # if given platform name and start_time, it should return all instrument which is activate at that range

        res = GetQuerySetMethod.get_instruments_by_deployment(platform_name=platform_name,
                                                              deployment_start_time=deployment_start_time)

        the_platform_id = get_platform_id(self.platform_dict_data, platform_name)

        expected_instrument_ids = []
        for the_dict in self.instrument_on_platform_dict_data:
            platform_id = the_dict["platform_id"]
            start_time_str = the_dict["start_time"]
            end_time_str = the_dict["end_time"]
            start_time_str_obj = time_str_to_time_obj(start_time_str)
            if end_time_str:
                end_time_str_obj = time_str_to_time_obj(end_time_str)

            else:
                end_time_str_obj = None

            if platform_id == the_platform_id:
                the_id = the_dict["instrument_id"]
                if the_id not in expected_instrument_ids:
                    if common_time_period(start_time_str_obj, end_time_str_obj, deployment_start_time_datetime,
                                          deployment_end_time_datetime):
                        expected_instrument_ids.append(the_dict["instrument_id"])

        self.assertEqual(get_objs_or_qs_ids_sorted(res), sorted(expected_instrument_ids))

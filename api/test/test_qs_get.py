from django.test import TestCase
from django.forms.models import model_to_dict
from datetime import datetime
from .create_mock_sensor_tracker_database import create_mock_database
from operator import itemgetter
from app_common.utilities.time_format_functions import str_to_timeobj, time_to_str, time_period_overlap

from api.core.qs_getter import GetQuerySetMethod
from .create_mock_sensor_tracker_database import replace_to_id, filter_out_create_day_modified_day
from .dictionary_search_functions import get_platform_by_name_serial, get_platform_by_serial, get_by_name, \
    get_by_given_id, get_by


def model_objs_to_dict_list(objs):
    ret_dict = []
    for o in objs:
        the_obj_dict = model_to_dict(o)
        for key, item in the_obj_dict.items():
            if isinstance(item, datetime):
                the_obj_dict[key] = time_to_str(item, time_str_format="%Y-%m-%dT%H:%M:%SZ")

        the_obj_dict = replace_to_id(filter_out_create_day_modified_day(the_obj_dict))
        ret_dict.append(the_obj_dict)

    return ret_dict


def get_platform_id(platform_dict, platform_name):
    the_platform_id = None
    for x in platform_dict:
        if x["name"] == platform_name:
            the_platform_id = x["id"]
    return the_platform_id


def get_platform_content_by_name(platform_dict, platform_name):
    ret_list = []
    for x in platform_dict:
        if x["name"] == platform_name:
            ret_list.append(x)
    return ret_list


def time_str_to_time_obj(time_str):
    """Convert different format of time str into datetime obj

    :param time_str: time str
    :return: datetime obj
    """
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


def get_objs_or_qs_ids_sorted(qs_or_objs):
    ret_ids = []
    for obj in qs_or_objs:
        id = obj.id
        if id not in ret_ids:
            ret_ids.append(id)
    return sorted(ret_ids)


class QsGetTest(TestCase):
    def setUp(self):
        self.maxDiff = 19213
        self.database_json = create_mock_database()
        self.instrument_on_platform_dict_data = self.database_json["instrument_on_platform"]
        self.platform_dict_data = self.database_json["platform"]
        self.manufacturer_dict = self.database_json["manufacturer"]
        self.institution_dict = self.database_json["institution"]
        self.project = self.database_json["project"]
        self.power = self.database_json["power_type"]
        self.platform_type = self.database_json["platform_type"]
        self.deployment = self.database_json["deployment"]
        self.instrument = self.database_json["instrument"]
        self.sensor = self.database_json["sensor"]
        self.sensor_on_instrument = self.database_json["sensor_on_instrument"]

    def get_by_name_only_queries_function(self, the_query_function, the_name, sample_res_dict):
        if the_name:
            res_dict = model_objs_to_dict_list(the_query_function(name=the_name))
            expected_list = get_by_name(sample_res_dict, the_name)
            self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))
        else:
            res_dict = model_objs_to_dict_list(the_query_function())
            self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(sample_res_dict, key=itemgetter('id')))

    """
    get_instruments_by_deployment test
    """

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
                    if time_period_overlap(start_time_str_obj, end_time_str_obj, deployment_start_time_datetime,
                                           deployment_end_time_datetime):
                        expected_instrument_ids.append(the_dict["instrument_id"])

        self.assertEqual(get_objs_or_qs_ids_sorted(res), sorted(expected_instrument_ids))

    def test_get_instrument_by_deployment_platform_name_and_start_time_with_end_time(self):
        platform_name = "otn200"
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
                    if time_period_overlap(start_time_str_obj, end_time_str_obj, deployment_start_time_datetime,
                                           deployment_end_time_datetime):
                        expected_instrument_ids.append(the_dict["instrument_id"])

        self.assertEqual(get_objs_or_qs_ids_sorted(res), sorted(expected_instrument_ids))

    """
    get platform test
    """

    def test_get_platforms_by_platform_name(self):
        platform_name = "scotia"
        res = GetQuerySetMethod.get_platforms(platform_name=platform_name)
        expect_platform_data = get_platform_content_by_name(self.platform_dict_data, platform_name)
        ret_dict = model_objs_to_dict_list(res)
        self.assertEqual(len(ret_dict), len(expect_platform_data))
        self.assertEqual(sorted(ret_dict, key=itemgetter('id')), sorted(expect_platform_data, key=itemgetter('id')))

    def test_get_platforms_by_platform_name_serial(self):
        platform_name = "scotia"
        serial = "711"
        wrong_serial_number = "712"
        res1 = GetQuerySetMethod.get_platforms(platform_name=platform_name, serial_number=wrong_serial_number)
        ret_dict = model_objs_to_dict_list(res1)
        expected_res_wrong_serial_version = get_platform_by_name_serial(self.platform_dict_data, platform_name,
                                                                        wrong_serial_number)
        self.assertEqual(sorted(ret_dict, key=itemgetter('id')),
                         sorted(expected_res_wrong_serial_version, key=itemgetter('id')))
        res2 = GetQuerySetMethod.get_platforms(platform_name=platform_name, serial_number=wrong_serial_number)
        ret_dict2 = model_objs_to_dict_list(res2)
        expected_res_serial = get_platform_by_name_serial(self.platform_dict_data, platform_name,
                                                          serial)
        self.assertEqual(sorted(ret_dict2, key=itemgetter('id')),
                         sorted(expected_res_serial, key=itemgetter('id')))

    def test_get_platforms_by_platform_serial(self):
        serial_number = "711"
        res = GetQuerySetMethod.get_platforms(serial_number=serial_number)
        expect_platform_data = get_platform_by_serial(self.platform_dict_data, serial_number)
        ret_dict = model_objs_to_dict_list(res)
        self.assertEqual(len(ret_dict), len(expect_platform_data))
        self.assertEqual(sorted(ret_dict, key=itemgetter('id')), sorted(expect_platform_data, key=itemgetter('id')))

    def test_get_all_platforms(self):
        res = GetQuerySetMethod.get_platforms()
        ret_dict = model_objs_to_dict_list(res)
        self.assertEqual(len(ret_dict), len(self.platform_dict_data))
        self.assertEqual(sorted(ret_dict, key=itemgetter('id')), sorted(self.platform_dict_data, key=itemgetter('id')))

    """
    get_manufacturer test
    """

    def test_get_manufacturer(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_manufacturer, None,
                                               self.manufacturer_dict)

    def test_get_manufacturer_by_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_manufacturer, "Liquid Robotics",
                                               self.manufacturer_dict)

    def test_get_manufacturer_by_invalid_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_institutions, "Fake Name", self.institution_dict)

    """
    get_institutions test
    """

    def test_get_institutions(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_institutions, None, self.institution_dict)

    def test_get_institutions_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_institutions, "MEOPAR", self.institution_dict)

    def test_get_institutions_with_different_case_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_institutions, "meopar", self.institution_dict)

    def test_get_institutions_with_no_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_institutions, "Fake Name", self.institution_dict)

    """
    get_project test
    """

    def test_get_project(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_project, None, self.project)

    def test_get_project_with_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_project, "HFX", self.project)

    def test_get_project_with_different_case_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_project, "hfx", self.project)

    def test_get_project_with_invalid_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_project, "Fake Name", self.project)

    """
    get power test
    """

    def test_get_power(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_power, None, self.power)

    def test_get_power_with_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_power, "Alkaline", self.power)

    def test_get_power_with_different_case_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_power, "alkaline", self.power)

    def test_get_power_with_invalid_name(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_power, "Fake Name", self.power)

    """
    get_platform_type test 
    """

    def test_get_platform_type(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_platform_type, None, self.platform_type)

    def test_get_platform_type_model(self):
        model = "Mooring"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_platform_type(model=model))
        expected_list = get_by_given_id(self.platform_type, [10])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_platform_type_model_how(self):
        model = "slocum"
        how = "contains"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_platform_type(model=model, how=how))
        expected_list = get_by_given_id(self.platform_type, [1, 6, 9])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

        model2 = "Slocum*"
        how2 = "regex"
        res_dict2 = model_objs_to_dict_list(GetQuerySetMethod.get_platform_type(model=model2, how=how2))
        expected_list2 = get_by_given_id(self.platform_type, [1, 6, 9])
        self.assertEqual(sorted(res_dict2, key=itemgetter('id')), sorted(expected_list2, key=itemgetter('id')))

    """
    get_deployments_by_platform_type test
    """

    def test_get_deployments_by_platform_type(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_deployments_by_platform_type, None,
                                               self.deployment)

    def test_get_deployments_by_platform_type_model(self):
        model = "Slocum Glider G2"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments_by_platform_type(model=model))
        expected_list = get_by_given_id(self.deployment, [31, 2263,23239])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

        model2 = "Slocum"
        res_dict2 = model_objs_to_dict_list(
            GetQuerySetMethod.get_deployments_by_platform_type(model=model2, how="contains"))
        expected_list2 = get_by_given_id(self.deployment, [31, 2263, 23234, 23239])
        self.assertEqual(sorted(res_dict2, key=itemgetter('id')), sorted(expected_list2, key=itemgetter('id')))

        model3 = "aq"
        res_dict3 = model_objs_to_dict_list(
            GetQuerySetMethod.get_deployments_by_platform_type(model=model3, how="contains"))
        expected_list3 = get_by_given_id(self.deployment, [])
        self.assertEqual(sorted(res_dict3, key=itemgetter('id')), sorted(expected_list3, key=itemgetter('id')))

    """
    get_deployments test
    """

    def test_get_deployments(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_deployments, None,
                                               self.deployment)

    def test_get_deployment_by_wmo_id(self):
        wmo_id = 1
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(wmo_id=wmo_id))
        expected_list = get_by_given_id(self.deployment, [])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_platform_name(self):
        platform_name = "dal556"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(platform_name=platform_name))
        expected_list = get_by_given_id(self.deployment, [31])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_institution_name(self):
        institution_name = "OTN"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(institution_name=institution_name))
        expected_list = get_by_given_id(self.deployment, [31, 2263])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_project_name(self):
        project_name = "Halifax Line Monitoring"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(project_name=project_name))
        expected_list = get_by_given_id(self.deployment, [31])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_title(self):
        title = "31"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(title=title))
        expected_list = get_by_given_id(self.deployment, [31])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_testing(self):
        testing_mission = True
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(testing_mission=testing_mission))
        expected_list = get_by_given_id(self.deployment, [])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_start_time(self):
        start_time = "2019-09-26T13:19:38Z"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(start_time=start_time))
        expected_list = get_by_given_id(self.deployment, [23239])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    def test_get_deployment_by_deployment_number(self):
        deployment_number = 108
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_deployments(deployment_number=deployment_number))
        expected_list = get_by_given_id(self.deployment, [23239])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    """
    get_instrument_by_platform
    """

    def test_get_instrument_by_platform(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_instrument_by_platform, None,
                                               self.instrument)

    def test_get_instrument_by_platform_name(self):
        platform_name = "otn200"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_instrument_by_platform(platform_name=platform_name))
        expected_list = get_by_given_id(self.instrument, [13, 14, 58, 41, 19, 18, 57, 15, 16, 20])
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    """
    get_instrument
    """

    def test_get_instrument(self):
        self.get_by_name_only_queries_function(GetQuerySetMethod.get_instrument, None,
                                               self.instrument)

    def test_get_instrument_by_identifier(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument, {"identifier": "sci_m"}, self.instrument)

    def test_get_instrument_by_short_name(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument, {"short_name": "flight commanded"}, self.instrument)

    def test_get_instrument_by_long_name(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument, {"long_name": "flight computer commanded"},
                                  self.instrument)

    def test_get_instrument_by_manufacturer(self):
        # todo make more complex search function for it.
        ...

    def test_get_instrument_by_serial(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument, {"serial": "200"}, self.instrument)

    def get_by_function_test(self, the_query_function, the_variable_dict, sample_res_dict):
        res_dict = model_objs_to_dict_list(the_query_function(**the_variable_dict))
        expected_list = get_by(sample_res_dict, the_variable_dict)
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    """
    get_instruments test
    """

    """
    _get_instrument_on_platform
    """

    """
    get_instrument_on_platform_by_platform test
    """

    def test_get_instrument_on_platform_by_platform(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument_on_platform_by_platform, {},
                                  self.instrument_on_platform_dict_data)

    def test_get_instrument_on_platform_by_platform_by_platform_name(self):

        platform_name = "otn200"
        res_dict = model_objs_to_dict_list(
            GetQuerySetMethod.get_instrument_on_platform_by_platform(platform_name=platform_name))
        expected_list = get_by_given_id(self.instrument_on_platform_dict_data,
                                        [13, 14, 8, 22, 7, 36, 37, 38, 39, 6, 40, 41, 10, 42, 43, 9, 44, 45, 46, 47, 48,
                                         49, 50, 51, 52])
        self.assertEqual(len(res_dict), len(expected_list))
        self.assertEqual(sorted(res_dict, key=itemgetter('id')), sorted(expected_list, key=itemgetter('id')))

    """
    get_instrument_on_platform_by_instrument test
    """

    def test_get_instrument_on_platform_by_instrument(self):
        self.get_by_function_test(GetQuerySetMethod.get_instrument_on_platform_by_instrument, {},
                                  self.instrument_on_platform_dict_data)

    def test_instrument_on_platform_by_instrument_by_identifier(self):
        ...

    def test_instrument_on_platform_by_instrument_by_serial(self):
        ...

    """
    get_sensor_on_instrument
    """

    def test_get_sensor_on_instrument(self):
        self.get_by_function_test(GetQuerySetMethod.get_sensor_on_instrument, {},
                                  self.sensor_on_instrument)

    def test_get_sensor_on_instrument_by_platform_name(self):
        platform_name = "otn200"
        platform_dict = get_by(self.platform_dict_data, {"name": platform_name})
        platform_ids = []
        for key, item in enumerate(platform_dict):
            platform_ids.append(item["id"])

        instrument_id_list = []
        for the_id in platform_ids:
            res = get_by(self.instrument_on_platform_dict_data, {"platform_id": the_id})
            for i in res:
                if i["instrument_id"] not in instrument_id_list:
                    instrument_id_list.append(i["instrument_id"])

        expected_sensor_on_instrument_dict_list = []
        for instrument_id in instrument_id_list:
            res = get_by(self.sensor_on_instrument, {"instrument_id": instrument_id})
            expected_sensor_on_instrument_dict_list.extend(res)

        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_sensor_on_instrument(platform_name=platform_name))

        self.assertEqual(len(res_dict), len(expected_sensor_on_instrument_dict_list))
        self.assertEqual(sorted(res_dict, key=itemgetter('id')),
                         sorted(expected_sensor_on_instrument_dict_list, key=itemgetter('id')))

    def test_get_sensor_on_instrument_by_instrument_identifier(self):
        instrument_identifier = "sci_m"
        instrument_dict_list = get_by(self.instrument, {"identifier": instrument_identifier})
        instrument_ids_list = []
        for x in instrument_dict_list:
            instrument_ids_list.append(x["id"])

        expected_sensor_on_instrument_list = []
        for x in instrument_ids_list:
            expected_sensor_on_instrument_list.extend(get_by(self.sensor_on_instrument, {"instrument_id": x}))

        res_dict = model_objs_to_dict_list(
            GetQuerySetMethod.get_sensor_on_instrument(instrument_identifier=instrument_identifier))

        self.assertEqual(len(res_dict), len(expected_sensor_on_instrument_list))
        self.assertEqual(sorted(res_dict, key=itemgetter('id')),
                         sorted(expected_sensor_on_instrument_list, key=itemgetter('id')))

    def test_get_sensor_on_instrument_by_platform_name_deployment_start_time(self):
        platform_name = "otn200"
        deployment_start_time = "2019-09-26T13:19:38Z"
        res_dict = model_objs_to_dict_list(GetQuerySetMethod.get_sensor_on_instrument(platform_name=platform_name,
                                                                                      deployment_start_time=deployment_start_time))

        platform_dict = get_by(self.platform_dict_data, {"name": platform_name})
        deployment_input = []
        for key, item in enumerate(platform_dict):
            deployment_input.append({"platform_id": item["id"], "start_time": deployment_start_time})

        deployment_dict_list = []

        for x in deployment_input:
            deployment_dict_list.extend(get_by(self.deployment, x))

        instrument_id_list = []
        for deployment_dict in deployment_dict_list:
            res = get_by(self.instrument_on_platform_dict_data, {"platform_id": deployment_dict["platform_id"]})
            d_start_time = deployment_dict["start_time"]
            d_end_time = deployment_dict["end_time"]
            for i in res:
                i_start_time = i["start_time"]
                i_end_time = i["end_time"]
                if i["instrument_id"] not in instrument_id_list and time_period_overlap(
                        time_str_to_time_obj(d_start_time), time_str_to_time_obj(d_end_time),
                        time_str_to_time_obj(i_start_time), time_str_to_time_obj(i_end_time)):
                    instrument_id_list.append(i["instrument_id"])

        expected_sensor_on_instrument_dict_list = []
        for instrument_id in instrument_id_list:
            res = get_by(self.sensor_on_instrument, {"instrument_id": instrument_id})
            expected_sensor_on_instrument_dict_list.extend(res)
        self.assertEqual(len(res_dict), len(expected_sensor_on_instrument_dict_list))
        self.assertEqual(sorted(res_dict, key=itemgetter('id')),
                         sorted(expected_sensor_on_instrument_dict_list, key=itemgetter('id')))

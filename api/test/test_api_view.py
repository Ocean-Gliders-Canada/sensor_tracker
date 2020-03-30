import copy

from django.test import TestCase

from rest_framework.test import APIRequestFactory

from .create_mock_sensor_tracker_database import create_mock_database, replace_to_id
from ..views import *


class ApiTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.database_json = create_mock_database()

    def test_manufacturer_api_view(self):
        # Test Manufacturer API
        view = GetManufacturer.as_view({'get': 'list'})

        # Test Manufacturer List
        self.the_list_test(view, "manufacturer")

        # Test get manufacturer by parameter
        self.the_parameter_get_test(view, "manufacturer", {"name": "Teledyne Webb"})



    def test_get_APIs(self):

        # Test Project API
        view = GetProject.as_view({'get': 'list'})
        # Test Project list
        self.the_list_test(view, "project")

        # Test get project by parameter
        self.the_parameter_get_test(view, "project", {"name": "HFX"})

        # Test Power Type API
        view = GetPower.as_view({'get': 'list'})
        # Test power list
        self.the_list_test(view, "power", "power_type")

        # Test get power by parameter
        self.the_parameter_get_test(view, "power", {"name": "Rechargeable lithium"}, "power_type")

        # Test Platform Type API
        view = GetPlatformType.as_view({'get': 'list'})
        # Test platform type list
        self.the_list_test(view, "platform_type")

        # get platform type by parameter
        self.the_parameter_get_test(view, "platform_type", {"model": "Slocum Glider G1"})

        # special gets for platform type by using how option
        self.special_platform_type_test(view, "platform_type")
        # Test Institution API
        view = GetInstitutions.as_view({'get': 'list'})

        # Test Institution List
        self.the_list_test(view, "institution")

        # Test get institution by parameter
        self.the_parameter_get_test(view, "institution", {"name": "OTN"})

        # Test Platform API
        view = GetPlatform.as_view({'get': 'list'})

        # Test Platform List
        self.the_list_test(view, "platform")

        # Test get platform by parameter
        self.the_parameter_get_test(view, "platform", {"serial_number": "200"})

        # platform's special get
        self.special_platform_test(view, "platform")

        # Test Deployment API
        view = GetDeployment.as_view({'get': 'list'})

        # Test Deployment List
        self.the_list_test(view, "deployment")

        # Test get Deployment by parameter
        self.the_parameter_get_test(view, "deployment", {"deployment_number": 92})
        self.the_parameter_get_test(view, "deployment", {"testing_mission": False})

        # Test Deployment special parameter
        self.special_deployment_get(view)

        # Test Instrument on Platform API
        view = GetInstrumentOnPlatform.as_view({'get': 'list'})
        # Test Instrument on Platform List
        self.the_list_test(view, "instrument_on_platform")

        # Test get Instrument on platform by parameter
        self.instrument_on_platform_test(view)
        self.instrument_on_platform_test(view)

        # Test Instrument API
        view = GetInstrument.as_view({'get': 'list'})

        # Test Instrument List
        self.the_list_test(view, "instrument")

        # Test get Instrument by parameter
        self.the_parameter_get_test(view, "instrument", {"identifier": "c"})
        self.the_parameter_get_test(view, "instrument", {"long_name": "flight computer commanded"})
        self.the_parameter_get_test(view, "instrument", {"short_name": "science measured"})
        self.the_parameter_get_test(view, "instrument", {"serial": "007"})

        # Test Sensor API
        view = GetSensor.as_view({'get': 'list'})

        # get sensor by parameter
        self.the_parameter_get_test(view, "sensor", {"identifier": "COND"})
        self.the_parameter_get_test(view, "sensor", {"long_name": "Zero A/D"})

        # get special sensor by parameter
        self.the_sensor_test(view)

        # Test Sensor On Instrument API
        view = GetSensorOnInstrument.as_view({'get': 'list'})

        # Test Sensor On Instrument API
        self.the_list_test(view, "sensor_on_instrument")

        # test sensor on instrument special search
        self.the_sensor_on_instrument_test(view)

    def the_sensor_test(self, view):
        platform_name = "otn200"
        request = self.factory.get(url_the_keyword("sensor"), {"platform_name": platform_name})
        data_list = view(request).data["results"]
        expect_result = self.database_json["instrument_on_platform"]
        platform_data_list = self.database_json["platform"]
        expected_platform_json = None
        for x in platform_data_list:
            if x["name"] == platform_name:
                expected_platform_json = x
                break
        instrument_on_platform_data_list = self.database_json["instrument_on_platform"]
        expected_instrument_on_platform_list = []
        for x in instrument_on_platform_data_list:
            if x["platform_id"] == expected_platform_json["id"]:
                expected_instrument_on_platform_list.append(x)

        instrument_id_list = []
        for x in expected_instrument_on_platform_list:
            instrument_id_list.append(x["instrument_id"])
        expected_sensor_on_instrument_list = []
        for x in self.database_json["sensor_on_instrument"]:
            if x["instrument_id"] in instrument_id_list:
                expected_sensor_on_instrument_list.append(x)
        sensor_id_list = [x["sensor_id"] for x in expected_sensor_on_instrument_list]
        sensor_list = []
        for x in self.database_json["sensor"]:
            if x["id"] in sensor_id_list:
                sensor_list.append(x)

        self.data_list_compare(data_list, sensor_list)

    def the_sensor_on_instrument_test(self, view):
        platform_name = "otn200"
        request = self.factory.get(url_the_keyword("sensor_on_instrument"), {"platform_name": platform_name})
        data_list = view(request).data["results"]
        expect_result = self.database_json["sensor_on_instrument"]
        platform_data_list = self.database_json["platform"]
        expected_platform_json = None
        for x in platform_data_list:
            if x["name"] == platform_name:
                expected_platform_json = x
                break
        instrument_on_platform_data_list = self.database_json["instrument_on_platform"]
        expected_instrument_on_platform_list = []
        for x in instrument_on_platform_data_list:
            if x["platform_id"] == expected_platform_json["id"]:
                expected_instrument_on_platform_list.append(x)

        instrument_id_list = []

        for x in expected_instrument_on_platform_list:
            instrument_id_list.append(x["instrument_id"])
        expected_sensor_on_instrument_list = []
        for x in self.database_json["sensor_on_instrument"]:
            if x["instrument_id"] in instrument_id_list:
                expected_sensor_on_instrument_list.append(x)
        self.data_list_compare(data_list, expected_sensor_on_instrument_list)

    def test_get_istruments_by_deployment(self, view):
        platform_name = "otn200"
        request = self.factory.get(url_the_keyword("instrument"),
                                   {"platform_name": platform_name, "deployment_start_time": "2019-09-25"})
        data_list = view(request).data["results"]
        print(data_list)

    def instrument_on_platform_test(self, view):
        platform_name = "otn200"
        request = self.factory.get(url_the_keyword("instrument_on_platform"), {"platform_name": platform_name})
        data_list = view(request).data["results"]

        platform_data_list = self.database_json["platform"]
        expected_platform_json = None
        for x in platform_data_list:
            if x["name"] == platform_name:
                expected_platform_json = x
                break
        instrument_on_platform_data_list = self.database_json["instrument_on_platform"]
        expected_instrument_on_platform_list = []
        for x in instrument_on_platform_data_list:
            if x["platform_id"] == expected_platform_json["id"]:
                expected_instrument_on_platform_list.append(x)
        self.data_list_compare(data_list, expected_instrument_on_platform_list)

        identifier = "SATHSE0211"
        request = self.factory.get(url_the_keyword("instrument_on_platform"), {"identifier": identifier})
        data_list = view(request).data["results"]
        instrument_data_list = self.database_json["instrument"]
        the_instrument_json = None
        for x in instrument_data_list:
            if x["identifier"] == identifier:
                the_instrument_json = x
                break
        the_expected_instrument = []
        for x in instrument_on_platform_data_list:
            if x["instrument_id"] == the_instrument_json["id"]:
                the_expected_instrument.append(x)
        self.data_list_compare(data_list, the_expected_instrument)

    def the_list_test(self, view, api_keyword, expected_result_keyword=None):
        request = self.factory.get(url_the_keyword(api_keyword), {"limit": 200})
        data_list = view(request).data["results"]
        if not expected_result_keyword:
            expected_result_keyword = de_url_keyword(api_keyword)

        expect_result = self.database_json[expected_result_keyword]
        # Compare Length
        self.assertEqual(len(data_list), len(expect_result))
        # Compare the content detail
        self.data_list_compare(data_list, expect_result)

    def data_list_compare(self, data_list, expected_list):
        new_data_list = sorted(data_list, key=lambda k: k["id"])
        new_expected_data_list = sorted(expected_list, key=lambda k: k["id"])

        for index, value in enumerate(new_data_list):
            self.assertTrue(no_modified_date_and_create_compare(value, new_expected_data_list[index]))

    def the_parameter_get_test(self, view, api_keyword, payload, expected_result_keyword=None):
        request = self.factory.get(url_the_keyword(api_keyword), payload)
        data_list = view(request).data["results"]
        if not expected_result_keyword:
            expected_result_keyword = de_url_keyword(api_keyword)

        expect_result_list = self.database_json[expected_result_keyword]
        expect_result = search_the_result_base_on_payload(expect_result_list, payload)
        self.data_list_compare(data_list, expect_result)

    def filter_platform_type_in_json_by_contains(self, model):
        keyword = "platform_type"
        expect_result_list = self.database_json[de_url_keyword(keyword)]
        new_expect_results = []
        for x in expect_result_list:
            if model.lower() in x["model"].lower():
                new_expect_results.append(x)
        return new_expect_results

    def special_platform_type_test(self, view, api_keyword):
        how = "contains"
        model = "slocum"
        request = self.factory.get(url_the_keyword(api_keyword), {"model": model, "how": how})
        data_list = view(request).data["results"]

        new_expect_results = self.filter_platform_type_in_json_by_contains(model)
        self.data_list_compare(data_list, new_expect_results)

        pattern = '^Slocum\sGlider\sG\d$'
        how = "contains"
        request = self.factory.get(url_the_keyword(api_keyword), {"model": pattern, "how": how})
        data_list = view(request).data["results"]
        self.data_list_compare(data_list, new_expect_results)

    def filter_platform_by_model(self, model):
        platform_type_list = self.filter_platform_type_in_json_by_contains(model)
        platform_type_list_id_list = []
        for x in platform_type_list:
            platform_type_list_id_list.append(x["id"])

        expected_platform_list = []
        for x in self.database_json["platform"]:
            if x["platform_type_id"] in platform_type_list_id_list:
                expected_platform_list.append(x)
        return expected_platform_list

    def special_platform_test(self, view, api_keyword):
        model = "slocum"
        how = "contains"
        request = self.factory.get(url_the_keyword(api_keyword), {"model": model, "how": how})
        data_list = view(request).data["results"]

        expected_platform_list = self.filter_platform_by_model(model)
        self.data_list_compare(data_list, expected_platform_list)

    def special_deployment_get(self, view):
        model = "slocum"
        how = "contains"
        api_keyword = "deployment"
        request = self.factory.get(url_the_keyword(api_keyword), {"model": model, "how": how})
        data_list = view(request).data["results"]
        expected_platforms = self.filter_platform_by_model(model)
        expected_platforms_id = [x["id"] for x in expected_platforms]
        expected_deployments = []
        for x in self.database_json["deployment"]:
            if x["platform_id"] in expected_platforms_id:
                expected_deployments.append(x)
        self.data_list_compare(data_list, expected_deployments)


def search_the_result_base_on_payload(expected_list, payload):
    payload_len = len(payload)
    match_item = []
    for index, item in enumerate(expected_list):
        match_count = 0
        for key, value in payload.items():
            if item[key] == value:
                match_count += 1
            else:
                break
        if match_count == payload_len:
            match_item.append(item)
    return match_item


def no_modified_date_and_create_compare(item1, item2):
    new_item1 = copy.deepcopy(item1)
    new_item2 = copy.deepcopy(item2)
    new_item1.pop("created_date", None)
    new_item1.pop("modified_date", None)
    new_item2.pop("created_date", None)
    new_item2.pop("modified_date", None)
    new_item1 = replace_to_id(new_item1)
    compare = new_item1 == new_item2
    return compare


def url_the_keyword(keyword):
    new_keyword = keyword
    if not new_keyword.startswith('/'):
        new_keyword = '/' + new_keyword
    if not new_keyword.endswith('/'):
        new_keyword = new_keyword + '/'
    return new_keyword


def de_url_keyword(keyword):
    new_keyword = keyword
    if new_keyword.startswith('/'):
        new_keyword = new_keyword[1:]
    if new_keyword.endswith('/'):
        new_keyword = new_keyword[:-1]
    return new_keyword

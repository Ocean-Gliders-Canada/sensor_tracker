from django.test import TestCase
from api.core.api_base import ApiBaseView
from api.core.exceptions import VariableError, InvalidParameterError

from unittest.mock import MagicMock


class TestApiBase(TestCase):
    def setUp(self):
        self.test_api_view = ApiBaseView(test=True)
        # self.test_api_view.serializer_class = serializer.ManufacturerSerializer

    def test_check_for_mutual_exclusion_success(self):
        self.test_api_view.accept_option = {
            "identifier": "The name used to identify this instrument in the raw data.",
            "short_name": "The short, general name for the instrument.",
            "long_name": "The full name for the instrument",
            "serial": "The serial number of Instrument",
            "platform_name": "The name of platform that the instrument attach to",
            "deployment_start_time": "The start time of the deployment"
        }
        self.test_api_view.mutual_exclusion = (
            ["identifier", "short_name", "long_name", "serial"], ["platform_name", "start_time"])
        try:
            self.test_api_view._check_for_mutual_exclusion(["identifier", "short_name"])
        except InvalidParameterError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_check_for_mutual_exclusion_failed(self):
        self.test_api_view.accept_option = {
            "identifier": "The name used to identify this instrument in the raw data.",
            "short_name": "The short, general name for the instrument.",
            "long_name": "The full name for the instrument",
            "serial": "The serial number of Instrument",
            "platform_name": "The name of platform that the instrument attach to",
            "deployment_start_time": "The start time of the deployment"
        }
        self.test_api_view.mutual_exclusion = (
            ["identifier", "short_name", "long_name", "serial"], ["platform_name", "start_time"])
        try:
            self.test_api_view._check_for_mutual_exclusion(["long_name", "platform_name"])
        except VariableError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_check_for_unwelcome_parameter_success(self):
        self.test_api_view.accept_option = ["a", "b", "c"]
        try:
            self.test_api_view._unwelcome_parameter_check(["a", "c"])
        except InvalidParameterError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_check_for_unwelcome_parameter_failed(self):
        self.test_api_view.accept_basic = ["a", "b"]
        self.test_api_view.accept_option = ["c"]
        try:
            self.test_api_view._unwelcome_parameter_check(["a", "d"])
        except InvalidParameterError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_variable_check_success(self):
        self.test_api_view.accept_option = {
            "identifier": "The name used to identify this instrument in the raw data.",
            "short_name": "The short, general name for the instrument.",
            "long_name": "The full name for the instrument",
            "serial": "The serial number of Instrument",
            "platform_name": "The name of platform that the instrument attach to",
            "deployment_start_time": "The start time of the deployment"
        }
        self.test_api_view.mutual_exclusion = (
            ["identifier", "short_name", "long_name", "serial"], ["platform_name", "start_time"])
        try:
            self.test_api_view.variable_check(["a", "d"])
        except InvalidParameterError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            self.test_api_view.variable_check(["identifier", "platform_name"])
        except VariableError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            self.test_api_view.variable_check(["identifier", "short_name"])
        except InvalidParameterError:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_generate_input_argument(self):
        expected_value = {
            "a": "something1",
            "b": "something2"
        }
        self.test_api_view.accept_option = ["a", "b", "c", "d"]
        the_get = {
            "a": "something1",
            "b": "something2"
        }
        ret = self.test_api_view.generate_input_argument(the_get)
        self.assertEqual(expected_value, ret)
        expected_value2 = {
            "a": "something1",
            "b": "something2",
            "d": "something3"
        }
        the_get2 = {
            "a": "something1",
            "b": "something2",
            "d": "something3"
        }
        self.assertEqual(expected_value2, the_get2)

    def test__depth_limit_int_input(self):
        test_limit = -1
        test_limit2 = 11
        expected_ret = 0
        expected_ret2 = 10
        self.assertEqual(expected_ret, self.test_api_view._depth_limit(test_limit))
        self.assertTrue(expected_ret2, self.test_api_view._depth_limit(test_limit2))
        test_limit3 = 3
        self.assertTrue(test_limit3, self.test_api_view._depth_limit(test_limit3))

    def test__depth_limit_str_input(self):
        test_limit = "-1"
        test_limit2 = "11"
        expected_ret = 0
        expected_ret2 = 10
        self.assertEqual(expected_ret, self.test_api_view._depth_limit(test_limit))
        self.assertTrue(expected_ret2, self.test_api_view._depth_limit(test_limit2))
        test_limit3 = "3"
        self.assertTrue(int(test_limit3), self.test_api_view._depth_limit(test_limit3))

    def test_inner_initial(self):
        from api.core.serializer import PlatformDeploymentSerializer
        from api.core.qs_getter import GetQuerySetMethod
        self.test_api_view.accept_basic = {}
        self.test_api_view.accept_option = {
            "identifier": "The name used to identify this instrument in the raw data.",
            "short_name": "The short, general name for the instrument.",
            "long_name": "The full name for the instrument",
            "serial": "The serial number of Instrument",
            "platform_name": "The name of platform that the instrument attach to",
            "deployment_start_time": "The start time of the deployment"
        }
        self.test_api_view.serializer_class = PlatformDeploymentSerializer
        self.test_api_view.queryset_method = GetQuerySetMethod.get_instrument
        self.test_api_view.mutual_exclusion = (
            ["identifier", "short_name", "long_name", "serial"], ["platform_name", "start_time"])

        the_get = {
            "identifier": "something",
            "long_name": "something2"
        }
        the_mock_get = MagicMock()
        the_mock_get._request.GET = the_get
        self.test_api_view.request = the_mock_get
        expected_result = {
            "identifier": "something",
            "long_name": "something2",
            "depth": 0
        }
        ret = self.test_api_view._inner_initial()
        self.assertEqual(ret, expected_result)

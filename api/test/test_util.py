from unittest import TestCase
from api.core.util import change_to_case_insensitive_parameter


class TestUtil(TestCase):
    def setUp(self):
        self.sample_parameter1 = {
            "platform": "otn200",
            "institution": "otn"
        }
        self.expected_parameter1 = {
            "platform__iexact": "otn200",
            "institution__iexact": "otn"
        }
        self.selected_list = ["platform"]
        self.expected_parameter2 = {
            "platform__iexact": "otn200",
            "institution": "otn"
        }

    def test_convert_all_parameter(self):
        ret = change_to_case_insensitive_parameter(self.sample_parameter1)
        self.assertEqual(ret, self.expected_parameter1)

    def test_convert_parameter_from_list(self):
        ret = change_to_case_insensitive_parameter(self.sample_parameter1, self.selected_list)
        self.assertEqual(ret, self.expected_parameter2)

    def test_pass_invalid_parameter(self):
        """Should raise attribute error"""
        try:
            change_to_case_insensitive_parameter("otn200")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            change_to_case_insensitive_parameter(self.sample_parameter1, "random")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_pass_empty_parameter(self):
        """Should return empty dictionary"""
        ret = change_to_case_insensitive_parameter({})
        self.assertEqual(ret, dict())
        ret = change_to_case_insensitive_parameter({}, [])
        self.assertEqual(ret, dict())

    def test_no_change(self):
        """should return original list"""
        ret = change_to_case_insensitive_parameter(self.sample_parameter1, [])
        self.assertEqual(ret, self.sample_parameter1)

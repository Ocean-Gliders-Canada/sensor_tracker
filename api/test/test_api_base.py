from django.test import TestCase
from api.core.api_base import ApiBaseView
from api.core import serializer


class TestUtil(TestCase):
    def setUp(self):
        self.test_api_view = ApiBaseView(test=True)
        self.test_api_view.serializer_class = serializer.ManufacturerSerializer

    def test_check_for_mutual_exclusion(self):
        self.test_api_view.accept_basic = []
        self.test_api_view.accept_option = []
        self.test_api_view._unwelcome_parameter_check(["a"])

    def test_check_for_unwelcome_parameter(self):
        self.test_api_view.accept_basic = []
        self.test_api_view.accept_option = []

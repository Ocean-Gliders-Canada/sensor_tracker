from datetime import datetime
from instruments.model_form import SensorOnInstrumentForm
from django.test import SimpleTestCase, TestCase
from instruments.tests.create_mock_sensor_tracker_database import create_mock_database
from app_common.utilities.time_format_functions import str_to_timeobj


class SensorOnInstrumentFormTest(TestCase):
    def setUp(self):
        create_mock_database()

    def test_sensor_on_instrument_exists(self):
        data = {'instrument': 1, "sensor": 1, "start_time": datetime.now(), "end_time": None, "comment": "hj"}
        form = SensorOnInstrumentForm(data)
        form.is_valid()
        try:
            form.clean()
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_sensor_on_instrument_no_exist(self):
        data = {'instrument': 100, "sensor": 100, "start_time": datetime.now(), "end_time": None, "comment": "hj"}
        form = SensorOnInstrumentForm(data)
        try:
            form.is_valid()
            form.clean()
        except Exception as e:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_sensor_on_instrument_exists2(self):
        data = {'instrument': 1, "sensor": 2, "start_time": datetime.now(), "end_time": None, "comment": "hj"}
        form = SensorOnInstrumentForm(data)
        form.is_valid()
        try:
            form.clean()
        except Exception as e:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_sensor_on_instrument_exists3(self):
        data = {'instrument': 1, "sensor": 1,
                "start_time": str_to_timeobj("2017-11-15T16:25:32Z", time_format='%Y-%m-%dT%H:%M:%SZ'),
                "end_time": datetime.now(),
                "comment": "hj"}
        form = SensorOnInstrumentForm(data)
        form.is_valid()
        try:
            form.clean()
        except Exception as e:
            self.assertTrue(False)
        else:
            self.assertTrue(True)


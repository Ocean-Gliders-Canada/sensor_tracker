from django.contrib.admin.sites import AdminSite
from django.test import SimpleTestCase, TestCase
from django.test.utils import isolate_apps
from datetime import datetime
from instruments.admin import SensorOnInstrumentAdmin
from instruments.models import Instrument, SensorOnInstrument, Sensor, InstrumentOnPlatform, InstrumentComment, \
    InstrumentCommentBox
from instruments.tests.create_mock_sensor_tracker_database import create_mock_database
from instruments.admin import SensorOnInstrumentForm


class InstrumentAdminTests(TestCase):
    def setUp(self):
        create_mock_database()
        self.site = AdminSite()

    def test_create_sensor_on_instrument(self):
        now = datetime.now()
        ma = SensorOnInstrumentAdmin(model=SensorOnInstrument, admin_site=AdminSite())
        obj = SensorOnInstrument.objects.get(id=1)
        obj.end_time = now
        sensor_obj = Sensor.objects.get(id=1)
        self.assertNotEqual(sensor_obj.instrument, None)
        ma.save_model(obj=obj,
                      request=None, form=None, change=True)
        sensor_obj_after = Sensor.objects.get(id=1)

        self.assertEqual(sensor_obj_after.instrument, None)

        # save same thing again
        ma.save_model(obj=obj,
                      request=None, form=None, change=True)

    def test_delete_sensor_on_instrument(self):
        ...

    def test_modified_sensor_on_instrument(self):
        ...


class TestSensorOnInstrumentForm(TestCase):
    def setUp(self):
        create_mock_database()

    def test_create_new_form(self):
        form_data = {'instrument': 1, "sensor": 1, "start_time": datetime.now(), "end_time": None, "comment": "hj"}

        form = SensorOnInstrumentForm(data=form_data)
        # form.full_clean()
        # print(form.cleaned_data)
        print(form.errors)
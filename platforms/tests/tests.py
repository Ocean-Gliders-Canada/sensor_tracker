from datetime import datetime

from django import forms
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.admin.options import (
    HORIZONTAL, VERTICAL, ModelAdmin, TabularInline,
    get_content_type_for_model,
)
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.widgets import (
    AdminDateWidget, AdminRadioSelect, AutocompleteSelect,
    AutocompleteSelectMultiple,
)
from django.contrib.auth.models import User
from django.db import models
from django.forms.widgets import Select
from django.test import SimpleTestCase, TestCase
from django.test.utils import isolate_apps
from datetime import datetime
from instruments.admin import SensorOnInstrumentAdmin
from instruments.models import Instrument, SensorOnInstrument, Sensor, InstrumentOnPlatform, InstrumentComment, \
    InstrumentCommentBox
from instruments.tests.create_mock_sensor_tracker_database import create_mock_database


class InstrumentAdminTests(TestCase):
    def setUp(self):
        create_mock_database()
        self.site = AdminSite()

    def test_default_fields(self):
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



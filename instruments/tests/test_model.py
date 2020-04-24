from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment
from general.models import Manufacturer, Institution, Project
from instruments.models import Instrument, InstrumentCommentBox, InstrumentComment, InstrumentOnPlatform, Sensor
from datetime import datetime
from django.test import TestCase


class TestInstrument(TestCase):

    def setUp(self):
        self.identifier = "test_identifier"
        self.short_name = "test url"
        self.long_name = "test_long"
        self.manufacturer_name = "test_manufacturer"
        self.manufacturer = Manufacturer.objects.create(name=self.manufacturer_name)
        self.serial = "test_serial"

        Instrument.objects.create(identifier=self.identifier, short_name=self.short_name)
        Instrument.objects.create(identifier=self.identifier, short_name=self.short_name, long_name=self.long_name)
        Instrument.objects.create(identifier=self.identifier, short_name=self.short_name, serial=self.serial)
        Instrument.objects.create(identifier=self.identifier, short_name=self.short_name, long_name=self.long_name,
                                  serial=self.serial)

    def test_institution_str(self):
        institution_obj_1 = Instrument.objects.get(id=1)
        expected_str1 = self.identifier + " - " + self.short_name
        self.assertEqual(expected_str1, institution_obj_1.__str__())
        institution_obj_2 = Instrument.objects.get(id=2)
        expected_str2 = self.identifier + " - " + self.short_name + " - " + self.long_name
        self.assertEqual(expected_str2, institution_obj_2.__str__())
        institution_obj_3 = Instrument.objects.get(id=3)
        expected_str3 = self.identifier + " - " + self.short_name + " - " + self.serial
        self.assertEqual(expected_str3, institution_obj_3.__str__())
        institution_obj_4 = Instrument.objects.get(id=4)
        expected_str4 = self.identifier + " - " + self.short_name + " - " + self.long_name + " - " + self.serial
        self.assertEqual(expected_str4, institution_obj_4.__str__())


class TestInstrumentOnPlatform(TestCase):
    def setUp(self):
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"

        self.manufacturer_name = "test_manufacturer"
        self.manufacturer = Manufacturer.objects.create(name=self.manufacturer_name)

        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.identifier = "test_identifier"
        self.short_name = "test url"
        self.long_name = "test_long"

        self.serial = "test_serial"

        self.instrument = Instrument.objects.create(identifier=self.identifier, short_name=self.short_name)
        self.date_string = "2012-12-12 10:10:10"
        self.start_time_obj = datetime.strptime(self.date_string, '%Y-%m-%d %H:%M:%S')
        InstrumentOnPlatform.objects.create(instrument=self.instrument, platform=self.platform,
                                            start_time=self.start_time_obj)

    def test_instrument_on_platform_str(self):
        expected_str = self.identifier + " - " + self.short_name + " - " + self.test_name + " - " + self.test_serial_number + " - " + self.date_string + "+00:00"
        instrument_on_platform_obj = InstrumentOnPlatform.objects.get(id=1)
        self.assertEqual(expected_str, instrument_on_platform_obj.__str__())


class TestSensor(TestCase):

    def setUp(self):
        self.identifier = "test_identifier"
        Sensor.objects.create(identifier=self.identifier)

    def test_sensor_str(self):
        sensor_obj = Sensor.objects.get(id=1)
        expected_str = self.identifier
        self.assertEqual(expected_str, sensor_obj.__str__())

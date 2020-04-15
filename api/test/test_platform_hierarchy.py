from django.test import TestCase
from datetime import datetime
from general.models import Institution, Manufacturer, Project
from instruments.models import Sensor, Instrument, InstrumentOnPlatform, SensorOnInstrument
from platforms.models import Platform, PlatformDeployment, PlatformType, PlatformPowerType
from ..core.platform_hierarchy import GetHierarchy
from django.utils import timezone
import datetime


class HierarchyTest(TestCase):

    def setUp(self):
        self.maxDiff = None
        date = datetime.datetime.now(tz=timezone.utc)
        manufacturer = Manufacturer.objects.create(name='test_manufacturer_name')
        institution = Institution.objects.create(name='test_institution_name')
        platform_power_type = PlatformPowerType.objects.create(name='test_paltform_power_type')
        platform_type = PlatformType.objects.create(model='test_platform_type', manufacturer=manufacturer)
        platform1 = Platform.objects.create(name='test_platform_name', wmo_id=1, serial_number='test_serial_number',
                                            institution=institution, platform_type=platform_type)
        project = Project.objects.create(name='test_project_name')
        PlatformDeployment.objects.create(wmo_id=10, deployment_number=10, platform=platform1, institution=institution,
                                          project=project, power_type=platform_power_type,
                                          start_time=date)
        instrument1 = Instrument.objects.create(identifier='test_instrument_identifier', serial='test_serial')
        # instrument1.created_date = date
        # instrument1.save()
        InstrumentOnPlatform.objects.create(instrument=instrument1, platform=platform1, start_time=date,)
        sensor1 = Sensor.objects.create(identifier='1', long_name='long')

        sensor2 = Sensor.objects.create(identifier='2', long_name='long')

        SensorOnInstrument.objects.create(instrument=instrument1, sensor=sensor1, start_time=date)
        SensorOnInstrument.objects.create(instrument=instrument1, sensor=sensor2, start_time=date)

    def test_get_sensors_list(self):
        get_hierarchy = GetHierarchy()
        res = get_hierarchy.get_sensors_list(Sensor.objects.all())
        for sensor in res:
            sensor['modified_date'] = None
            sensor['created_date'] = None
            sensor['id'] = 'id'

        expect = [{'id': 'id', 'created_date': None, 'modified_date': None, 'identifier': '1',
                'long_name': 'long', 'standard_name': None, 'serial': None, 'instrument': None, 'type': 'f8',
                'units': None, 'precision': None, 'accuracy': None, 'resolution': None, 'valid_min': None,
                'valid_max': None, 'include_in_output': False, 'display_in_web_interface': False, 'comment': None},
               {'id': 'id', 'created_date': None, 'modified_date': None, 'identifier': '2',
                'long_name': 'long', 'standard_name': None, 'serial': None, 'instrument': None, 'type': 'f8',
                'units': None, 'precision': None, 'accuracy': None, 'resolution': None, 'valid_min': None,
                'valid_max': None, 'include_in_output': False, 'display_in_web_interface': False, 'comment': None}]
        self.assertEqual(expect, res)

    def test_get_instrument_list(self):
        get_hierarchy = GetHierarchy()
        res = get_hierarchy.get_instrument_list([Sensor.objects.all()], Instrument.objects.all())
        for ins_dict in res:
            ins_dict['modified_date'] = None
            ins_dict['created_date'] = None
            ins_dict['id'] = 'id'
            sensor_list = ins_dict['sensors_on_curr_instrument']
            for sensor in sensor_list:
                sensor['created_date'] = None
                sensor['modified_date'] = None
                sensor['id'] = 'id'
        expect = [{'id': 'id', 'created_date': None, 'modified_date': None, 'identifier': 'test_instrument_identifier',
                   'short_name': '', 'long_name': None, 'manufacturer': None, 'serial': 'test_serial',
                   'master_instrument': None, 'comment': None, 'sensors_on_curr_instrument': [
                {'id': 'id', 'created_date': None, 'modified_date': None, 'identifier': '1', 'long_name': 'long',
                 'standard_name': None, 'serial': None, 'instrument': None, 'type': 'f8', 'units': None,
                 'precision': None, 'accuracy': None, 'resolution': None, 'valid_min': None, 'valid_max': None,
                 'include_in_output': False, 'display_in_web_interface': False, 'comment': None},
                {'id': 'id', 'created_date': None, 'modified_date': None, 'identifier': '2', 'long_name': 'long',
                 'standard_name': None, 'serial': None, 'instrument': None, 'type': 'f8', 'units': None,
                 'precision': None, 'accuracy': None, 'resolution': None, 'valid_min': None, 'valid_max': None,
                 'include_in_output': False, 'display_in_web_interface': False, 'comment': None}]}]
        self.assertEqual(res, expect)

    def test_get_dict(self):
        get_hierarchy = GetHierarchy()
        sensors = Sensor.objects.first()
        sensor = Sensor._meta.fields
        sensor_fields = [sensor[i].name for i in range(len(sensor))]
        res = get_hierarchy.get_dict(sensors, sensor_fields)
        res['created_date'] = None
        res['modified_date'] = None
        res['id'] = 'id'
        expect = {'id': 'id', 'created_date': None, 'modified_date': None,
                  'identifier': '1', 'long_name': 'long', 'standard_name': None, 'serial': None, 'instrument': None,
                  'type': 'f8', 'units': None, 'precision': None, 'accuracy': None, 'resolution': None,
                  'valid_min': None, 'valid_max': None, 'include_in_output': False, 'display_in_web_interface': False,
                  'comment': None}
        self.assertEqual(res, expect)

    def test_get_sensor_and_instrument_qs(self):
        get_hierarchy = GetHierarchy()
        instrument_on_platform_qs = InstrumentOnPlatform.objects.all()
        instrument_qs, sensor_on_instrument_qs = get_hierarchy.get_sensor_and_instrument_qs(instrument_on_platform_qs)
        expect_instrument_qs = list(Instrument.objects.all())
        self.assertEqual(expect_instrument_qs, instrument_qs)

    def test_get_sensor_qs(self):
        get_hierarchy = GetHierarchy()
        instrument_on_platform_qs = InstrumentOnPlatform.objects.all()
        instrument_qs, sensor_on_instrument_qs = get_hierarchy.get_sensor_and_instrument_qs(instrument_on_platform_qs)
        res = get_hierarchy.get_sensor_qs(list(sensor_on_instrument_qs))
        expect_res = [list(Sensor.objects.all())]
        self.assertEqual(res, expect_res)



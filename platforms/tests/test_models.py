from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment
from general.models import Manufacturer, Institution, Project
from datetime import datetime
from django.test import TestCase


class PlatformTypeTest(TestCase):

    def setUp(self):
        self.test_manufacturer = "test_manufacturer"
        self.test_model_name = "test_model"
        Manufacturer.objects.create(name="test_manufacturer")
        PlatformType.objects.create(model="test_model", manufacturer_id=1)

    def test_platform_type_str(self):
        platform_type_obj = PlatformType.objects.get(id=1)
        expected_value = self.test_model_name + " - " + self.test_manufacturer
        self.assertEqual(expected_value, platform_type_obj.__str__())


class TestPlatform(TestCase):

    def setUp(self):
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)

    def test_platform_type_str(self):
        expected_platform_str = self.test_name + " - " + self.test_serial_number
        self.assertEqual(expected_platform_str, Platform.objects.get(id=1).__str__())


class TestPlatformPowerType(TestCase):
    def setUp(self):
        self.test_platform_power_name = "test_name"
        self.platform_power = PlatformPowerType.objects.create(name=self.test_platform_power_name)

    def test_platform_power_type(self):
        expected_str = self.test_platform_power_name
        self.assertEqual(expected_str, PlatformPowerType.objects.get(id=1))


class TestPlatformDeployment(TestCase):
    def setUp(self):
        self.deployment_number = 2
        self.title = "test_title"
        self.date_string = "2012-12-12 10:10:10"
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.test_project_name = "test_project_name"
        self.start_time_obj = datetime.strptime(self.date_string, '%Y-%m-%d %H:%M:%S')
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.test_platform_power_name = "test_name"
        self.platform_power = PlatformPowerType.objects.create(name=self.test_platform_power_name)
        self.project = Project.objects.create(name=self.test_project_name)
        self.platform_deployment = PlatformDeployment.objects.create(deployment_number=self.deployment_number,
                                                                     platform=self.platform,
                                                                     institution=self.institution,
                                                                     power_type=self.platform_power, title=self.title, start_time=self.start_time_obj, project=self.pr)

    def test_platform_deployment(self):
        ...



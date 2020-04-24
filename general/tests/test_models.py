from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment
from general.models import Manufacturer, Institution, Project
from datetime import datetime
from django.test import TestCase


class TestInstitution(TestCase):

    def setUp(self):
        self.institution_name = "test_name"
        self.url = "test url"

        self.street = "street name"
        self.city = "city name"
        Institution.objects.create(name=self.institution_name)

    def test_institution_str(self):
        expected_str = self.institution_name
        institution_obj = Institution.objects.get(id=1)
        self.assertEqual(expected_str, institution_obj.__str__())


class TestProject(TestCase):

    def setUp(self):
        self.project_name = "test_name"
        Project.objects.create(name=self.project_name)

    def test_project_str(self):
        project_obj = Project.objects.get(id=1)
        expected_str = self.project_name
        self.assertEqual(expected_str, project_obj.__str__())


class TestManufacturer(TestCase):

    def setUp(self):
        self.manufacturer_name = "test_name"
        Manufacturer.objects.create(name=self.manufacturer_name)

    def test_manufacturer_str(self):
        expected_manufacturer_str = self.manufacturer_name
        manufacturer_obj = Manufacturer.objects.get(id=1)
        self.assertEqual(expected_manufacturer_str, manufacturer_obj.__str__())

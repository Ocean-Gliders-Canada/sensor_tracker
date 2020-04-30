from platforms.models import PlatformType, Platform, PlatformPowerType, PlatformDeployment, PlatformDeploymentComment, \
    PlatformDeploymentCommentBox, PlatformComment, PlatformCommentBox
from general.models import Manufacturer, Institution, Project
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User


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
        self.deployment_number = "2"
        self.title = "test_title"
        self.date_string = "2012-12-12 10:10:10"
        self.date_string2 = "2011-11-11 10:10:10"
        self.date_string_short = "2012-12-12"
        self.date_string_short2 = "2011-11-11"
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.test_project_name = "test_project_name"
        self.start_time_obj = datetime.strptime(self.date_string, '%Y-%m-%d %H:%M:%S')
        self.start_time_ob2j = datetime.strptime(self.date_string2, '%Y-%m-%d %H:%M:%S')
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.test_platform_power_name = "test_name"
        self.platform_power = PlatformPowerType.objects.create(name=self.test_platform_power_name)
        self.project = Project.objects.create(name=self.test_project_name)
        self.platform_deployment1 = PlatformDeployment.objects.create(deployment_number=self.deployment_number,
                                                                      platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power, title=self.title,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project)
        self.platform_deployment2 = PlatformDeployment.objects.create(platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power, title=self.title,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project)
        self.platform_deployment3 = PlatformDeployment.objects.create(platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project)
        self.platform_deployment4 = PlatformDeployment.objects.create(platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project,
                                                                      end_time=self.start_time_ob2j)

    def test_platform_deployment(self):
        expected_str1 = self.deployment_number + " - " + self.title + " - " + self.test_name + " - " + self.date_string_short
        self.assertEqual(expected_str1, self.platform_deployment1.__str__())
        expected_str2 = self.title + " - " + self.test_name + " - " + self.date_string_short
        self.assertEqual(expected_str2, self.platform_deployment2.__str__())
        expected_str3 = self.test_name + " - " + self.date_string_short
        self.assertEqual(expected_str3, self.platform_deployment3.__str__())
        expected_str4 = self.test_name + " - " + self.date_string_short + " - " + self.date_string_short2
        self.assertEqual(expected_str4, self.platform_deployment4.__str__())


class TestPlatformDeploymentCommentBox(TestCase):
    def setUp(self):
        self.deployment_number = "2"
        self.title = "test_title"
        self.date_string = "2012-12-12 10:10:10"
        self.date_string2 = "2011-11-11 10:10:10"
        self.date_string_short = "2012-12-12"
        self.date_string_short2 = "2011-11-11"
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.test_project_name = "test_project_name"
        self.start_time_obj = datetime.strptime(self.date_string, '%Y-%m-%d %H:%M:%S')
        self.start_time_ob2j = datetime.strptime(self.date_string2, '%Y-%m-%d %H:%M:%S')
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.test_platform_power_name = "test_name"
        self.platform_power = PlatformPowerType.objects.create(name=self.test_platform_power_name)
        self.project = Project.objects.create(name=self.test_project_name)
        self.platform_deployment1 = PlatformDeployment.objects.create(deployment_number=self.deployment_number,
                                                                      platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power, title=self.title,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project)

        self.platform_deployment_box = PlatformDeploymentCommentBox.objects.create(
            platform_deployment=self.platform_deployment1)

    def test_platform_deployment_box(self):
        expected_str = self.deployment_number + " - " + self.title + " - " + self.test_name + " - " + self.date_string_short + " comment box"
        self.assertEqual(expected_str, self.platform_deployment_box.__str__())


class TestPlatformCommentBox(TestCase):
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
        self.platform_comment_box = PlatformCommentBox.objects.create(platform=self.platform)

    def test_platform_deployment_box(self):
        expected_platform_str = self.test_name + " - " + self.test_serial_number + " comment box"
        self.assertEqual(expected_platform_str, self.platform_comment_box.__str__())


class TestPlatformComment(TestCase):
    def setUp(self):
        my_user = User.objects.create(username='Testuser')
        self.comment = "test comment"
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.platform_comment_box = PlatformCommentBox.objects.create(platform=self.platform)
        self.platform_comment = PlatformComment.objects.create(user=my_user, comment=self.comment,
                                                               platform_comment_box=self.platform_comment_box)

    def test_platform_comment(self):
        self.assertEqual(str(1), self.platform_comment.id)


class TestPlatformDeploymentComment(TestCase):
    def setUp(self):
        self.deployment_number = "2"
        self.title = "test_title"
        self.date_string = "2012-12-12 10:10:10"
        self.date_string2 = "2011-11-11 10:10:10"
        self.date_string_short = "2012-12-12"
        self.date_string_short2 = "2011-11-11"
        self.test_name = "test_name"
        self.test_wmo_id = 2
        self.test_serial_number = "1"
        self.test_project_name = "test_project_name"
        self.start_time_obj = datetime.strptime(self.date_string, '%Y-%m-%d %H:%M:%S')
        self.start_time_ob2j = datetime.strptime(self.date_string2, '%Y-%m-%d %H:%M:%S')
        self.manufacturer = Manufacturer.objects.create(name="test_manufacturer")
        self.institution = Institution.objects.create(name="institution_name")
        self.platform_type = PlatformType.objects.create(model="test_model", manufacturer=self.manufacturer)
        self.platform = Platform.objects.create(name=self.test_name, wmo_id=self.test_wmo_id,
                                                serial_number=self.test_serial_number, platform_type=self.platform_type,
                                                institution=self.institution)
        self.test_platform_power_name = "test_name"
        self.platform_power = PlatformPowerType.objects.create(name=self.test_platform_power_name)
        self.project = Project.objects.create(name=self.test_project_name)
        self.platform_deployment1 = PlatformDeployment.objects.create(deployment_number=self.deployment_number,
                                                                      platform=self.platform,
                                                                      institution=self.institution,
                                                                      power_type=self.platform_power, title=self.title,
                                                                      start_time=self.start_time_obj,
                                                                      project=self.project)

        self.platform_deployment_box = PlatformDeploymentCommentBox.objects.create(
            platform_deployment=self.platform_deployment1)
        my_user = User.objects.create(username='Testuser')
        self.comment = "test comment"
        self.platform_deployment_comment = PlatformDeploymentComment.objects.create(user=my_user, comment=self.comment,
                                                                                    platform_deployment_comment_box=self.platform_deployment_box)

    def test_platform_deployment_comment(self):
        self.assertEqual(str(1), self.platform_deployment_comment.__str__())

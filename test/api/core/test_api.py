import datetime
import copy
from django.test import TestCase

from platforms.models import *
from instruments.models import *
from general.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.admin import User

from api.core.getter import (
    get_platform_by_name,
    get_sensors_by_platform,
    get_sensors_by_deployment,

    get_instrument_on_platform_by_platform,

    get_deployment_by_platform_name_start_time,
    get_platform_by_name,
    get_platform_type,
    get_platform_by_platform_type,
    get_deployments_by_platform,
    get_deployments_by_platform_type,
    get_instruments_by_deployment,
    get_deployment_comment,
    get_instruments,
    get_sensors,
    get_platform,
    get_manufacturer,
    get_institutions,
    get_project,
    get_power
)
from api.core.json_maker import get_apps_model_name, convert_model_to_dict_simple, convert_model_to_dict_recursive


class GetterTest(TestCase):
    def create_project_obj(self):
        self.project_obj1 = Project.objects.create(name="project_a")
        self.project_obj2 = Project.objects.create(name="project_b")

    def create_institution_obj(self):
        self.organization_objs = {}
        organization = ["OTN", "meopar", "dalhousie"]
        for org in organization:
            obj = Institution.objects.create(name=org)
            self.organization_objs[org] = obj

        return self.organization_objs

    def create_manufacturer_obj(self):
        self.manufacturer_obj = Manufacturer.objects.create(name="ceotr")

    def create_platform_type_objs(self):
        self.platform_type_objs = {}
        platform_types = ["mooring", "profiler", "VOS", "Slocum Glider G3", "Slocum Glider G1", "Slocum Glider G2",
                          "Wave Glider SV2"]
        for t in platform_types:
            obj = PlatformType.objects.create(model=t, manufacturer=self.manufacturer_obj)
            self.platform_type_objs[t] = obj
        return self.platform_type_objs

    def create_platform_objs(self):
        self.platform_obj1 = Platform.objects.create(name="cabot", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G3"])
        self.platform_obj2 = Platform.objects.create(name="scotia", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G3"])
        self.platform_obj3 = Platform.objects.create(name="Fundy", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G2"])
        self.platform_obj4 = Platform.objects.create(name="bond", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G1"])

    def create_deployments_objs(self):
        self.deployment_obj1 = PlatformDeployment.objects.create(
            deployment_number=1, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2017-03-12 12:00:00", end_time="2017-04-18 12:00:00")

        self.deployment_obj2 = PlatformDeployment.objects.create(
            deployment_number=2, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2018-05-12 12:00:00", end_time="2018-06-12 12:00:00")
        self.deployment_obj3 = PlatformDeployment.objects.create(
            deployment_number=3, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2019-05-12 12:00:00", end_time="2019-06-01 12:00:00")
        self.deployment_obj4 = PlatformDeployment.objects.create(
            deployment_number=4, platform=self.platform_obj2, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2019-06-12 12:00:00")

    def create_instrument_objs(self):
        self.instrument_obj1 = Instrument.objects.create(identifier="c", short_name="chi", long_name="chi shen me",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj2 = Instrument.objects.create(identifier="d", short_name="he",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj3 = Instrument.objects.create(identifier="e", short_name="wan",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj4 = Instrument.objects.create(identifier="f", short_name="le",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj5 = Instrument.objects.create(identifier="g", short_name="hai",
                                                         manufacturer=self.manufacturer_obj)

    def create_instrument_on_platform_objs(self):
        self.instrument_on_platform_obj1 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj1,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2017-03-12 12:00:00",
                                                                               end_time=None)
        self.instrument_on_platform_obj2 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj2,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2018-05-12 12:00:00",
                                                                               end_time="2018-06-12 12:00:00")
        self.instrument_on_platform_obj3 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj3,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2019-05-12 12:00:00",
                                                                               end_time="2019-06-01 12:00:00")
        self.instrument_on_platform_obj4 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj4,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2018-05-12 12:00:00",
                                                                               end_time=None)
        self.instrument_on_platform_obj5 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj5,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2019-06-12 12:00:00",
                                                                               end_time=None)

    def create_user(self):
        self.user_obj = User.objects.create(username="l", first_name="l", last_name="b", password='123')

    def create_deployment_commend_box_and_deployment_comments(self):
        self.deployment_comment_box_obj = PlatformDeploymentCommentBox.objects.create(
            platform_deployment=self.deployment_obj1)
        self.deployment_comment1 = PlatformDeploymentComment.objects.create(user=self.user_obj, comment="test_comment",
                                                                            platform_deployment_comment_box=self.deployment_comment_box_obj)
        self.deployment_comment1 = PlatformDeploymentComment.objects.create(user=self.user_obj, comment="test_comment2",
                                                                            platform_deployment_comment_box=self.deployment_comment_box_obj)

    def setUp(self):
        self.create_project_obj()
        self.create_institution_obj()
        self.create_manufacturer_obj()
        self.create_platform_type_objs()
        self.create_platform_objs()
        self.create_deployments_objs()
        self.create_instrument_objs()
        self.create_instrument_on_platform_objs()
        self.create_user()
        self.create_deployment_commend_box_and_deployment_comments()
        project_obj = Project.objects.create(name="the project")
        institution_obj = Institution.objects.create(name="institution A")
        manufacturer_obj = Manufacturer.objects.create(name="factory A")
        instrument_obj = Instrument.objects.create(identifier="a", short_name="short a", manufacturer=manufacturer_obj)
        instrument_obj2 = Instrument.objects.create(identifier="b", short_name="short a", manufacturer=manufacturer_obj)
        platform_type = PlatformType.objects.create(model="platform type model", manufacturer=manufacturer_obj)
        platform_obj = Platform.objects.create(name="platform a", institution=institution_obj,
                                               platform_type=platform_type)
        platform_obj2 = Platform.objects.create(name="platform b", institution=institution_obj,
                                                platform_type=platform_type)
        platform_deployment = PlatformDeployment.objects.create(platform=platform_obj, start_time="2019-03-12 14:55:02",
                                                                institution=institution_obj, project=project_obj,
                                                                deployment_number=1)

        platform_deployment2 = PlatformDeployment.objects.create(platform=platform_obj,
                                                                 start_time="2018-03-12 14:55:02",
                                                                 end_time="2018-03-13 14:55:02",
                                                                 institution=institution_obj, project=project_obj,
                                                                 deployment_number=1)

        instrument_on_platform = InstrumentOnPlatform.objects.create(instrument=instrument_obj, platform=platform_obj,
                                                                     start_time="2019-03-12 14:55:02")
        instrument_on_platform2 = InstrumentOnPlatform.objects.create(instrument=instrument_obj2,
                                                                      platform=platform_obj2,
                                                                      start_time="2019-03-12 14:55:02")

        instrument_on_platform3 = InstrumentOnPlatform.objects.create(instrument=instrument_obj2, platform=platform_obj,
                                                                      start_time="2019-03-12 14:55:02")

        self.sensor_obj1 = Sensor.objects.create(instrument=instrument_obj, identifier="sensor id",
                                                 long_name="sensor long name", standard_name="standard name")

        self.sensor_obj2 = Sensor.objects.create(instrument=instrument_obj, identifier="sensor_id2",
                                                 long_name="sensor long name2", standard_name="standard name2")

    def test_get_platform_by_name(self):
        obj = get_platform_by_name("cabot")
        self.assertEqual(obj.name, "cabot")
        obj2 = get_platform_by_name("some")
        if not obj2:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_sensors_by_platform(self):
        objs = get_sensors_by_platform('platform a')
        self.assertEqual(len(objs), 2)
        sensor_obj1 = objs[0]
        sensor_obj2 = objs[1]

        self.assertEqual(sensor_obj2.identifier, self.sensor_obj1.identifier)
        self.assertEqual(sensor_obj1.identifier, self.sensor_obj2.identifier)

        obj2s = get_sensors_by_platform("no_exist_platform")
        self.assertEqual(len(obj2s), 0)

        obj3s = get_sensors_by_platform("platform b")
        self.assertEqual(len(obj3s), 0)

    def test_get_instrument_on_platform_by_platform(self):
        objs = get_instrument_on_platform_by_platform("platform a")
        self.assertEqual(len(objs), 2)

    def test_get_platform_deployment_by_name_time(self):
        obj = get_deployment_by_platform_name_start_time("platform a", "2019-03-12 14:55:02")
        self.assertTrue(obj.deployment_number, 1)

    def test_get_sensors_by_deployment(self):
        sensors = get_sensors_by_deployment(platform_name="platform a", start_time="2019-03-12 14:55:02")
        sensors2 = get_sensors_by_deployment(platform_name="platform a", start_time="2018-03-12 14:55:02")
        self.assertEqual(len(sensors2), 0)

    def test_get_platform_type(self):
        # test match
        platform_type = get_platform_type("Slocum Glider G3")
        self.assertEqual(platform_type, [self.platform_type_objs["Slocum Glider G3"]])
        # test contains
        platform_type2 = get_platform_type("slocum", how="contains")
        self.assertEqual(len(platform_type2), 3)
        # test regex
        pattern = '^Slocum\sGlider\sG\d$'
        platform_type3 = get_platform_type(pattern, how="regex")
        self.assertEqual(len(platform_type3), 3)
        # test invalid input for match
        try:
            get_platform_type(1)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # test invalid input for contains
        try:
            get_platform_type([], how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(1.0, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(1, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type({}, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type((), how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(object(), how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # test invalid input for regex
        try:
            get_platform_type([], how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(1.0, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(1, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type({}, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type((), how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_type(object(), how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_platform_by_platform_type(self):
        platform_objs = get_platform_by_platform_type(model="Slocum", how="contains")
        self.assertEqual(len(platform_objs), 4)

        # test invalid input for match
        try:
            get_platform_type(1)
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # test invalid input for contains
        try:
            get_platform_by_platform_type([], how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(1.0, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(1, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type({}, how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type((), how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(object(), how="contains")
        except AttributeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        # test invalid input for regex
        try:
            get_platform_by_platform_type([], how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(1.0, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(1, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type({}, how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type((), how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

        try:
            get_platform_by_platform_type(object(), how="regex")
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_deployments_by_platform(self):
        deployments = get_deployments_by_platform("cabot")
        self.assertEqual(len(deployments), 3)

    def test_get_deployments_by_platform_type(self):
        deployments = get_deployments_by_platform_type("slocum", how="contains")
        self.assertEqual(len(deployments), 4)
        try:
            deployments2 = get_deployments_by_platform_type("asd")
        except ObjectDoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_get_deployment_comment(self):
        res = get_deployment_comment(platform_name="cabot", start_time="2017-03-12 12:00:00")
        print(res)

    def test_get_instrument(self):
        res = get_instruments(identifier='c')
        print(res)
        res = get_instruments(short_name='chi')
        print(res)
        res = get_instruments(long_name='chi shen me')
        print(res)
        res = get_instruments()
        print(res)

    def test_get_sensors(self):
        res = get_sensors()
        print(res)

    def test_get_platform(self):
        res = get_platform()
        print(res)

    def test_get_manufacturer(self):
        res = get_manufacturer()
        print(res)

    def test_get_institutions(self):
        res = get_institutions()
        print(res)

    def test_get_project(self):
        res = get_project()
        print(res)

    def test_get_power(self):
        res = get_power()
        print(res)


class JsonMakerTest(TestCase):

    def create_project_obj(self):
        self.project_obj1 = Project.objects.create(name="project_a")
        self.project_obj2 = Project.objects.create(name="project_b")

    def create_institution_obj(self):
        self.organization_objs = {}
        organization = ["OTN", "meopar", "dalhousie"]
        for org in organization:
            obj = Institution.objects.create(name=org)
            self.organization_objs[org] = obj

        return self.organization_objs

    def create_manufacturer_obj(self):
        self.manufacturer_obj = Manufacturer.objects.create(name="ceotr")

    def create_platform_type_objs(self):
        self.platform_type_objs = {}
        platform_types = ["mooring", "profiler", "VOS", "Slocum Glider G3", "Slocum Glider G1", "Slocum Glider G2",
                          "Wave Glider SV2"]
        for t in platform_types:
            obj = PlatformType.objects.create(model=t, manufacturer=self.manufacturer_obj)
            self.platform_type_objs[t] = obj
        return self.platform_type_objs

    def create_platform_objs(self):
        self.platform_obj1 = Platform.objects.create(name="cabot", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G3"])

    def create_instrument_objs(self):
        self.instrument_obj1 = Instrument.objects.create(identifier="c", short_name="chi",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj2 = Instrument.objects.create(identifier="w", short_name="wei",
                                                         manufacturer=self.manufacturer_obj,
                                                         master_instrument=self.instrument_obj1)

    def create_instrument_on_platform_objs(self):
        self.instrument_on_platform_obj1 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj1,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2017-03-12 12:00:00",
                                                                               end_time=None)
        self.instrument_on_platform_obj2 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj2,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2017-03-12 12:00:00",
                                                                               end_time=None)

    def create_deployments_objs(self):
        self.deployment_obj1 = PlatformDeployment.objects.create(
            deployment_number=1, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2017-03-12 12:00:00", end_time="2017-04-18 12:00:00")

        self.deployment_obj2 = PlatformDeployment.objects.create(
            deployment_number=2, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2018-05-12 12:00:00", end_time="2018-06-12 12:00:00")
        self.deployment_obj3 = PlatformDeployment.objects.create(
            deployment_number=3, platform=self.platform_obj1, project=self.project_obj1,
            institution=self.organization_objs["OTN"], start_time="2019-05-12 12:00:00", end_time="2019-06-01 12:00:00")

    def create_sensors(self):
        self.sensor_obj1 = Sensor.objects.create(instrument=self.instrument_obj1, identifier='m_depth',
                                                 long_name='m_depth', standard_name='depth')

    def setUp(self):
        self.create_project_obj()
        self.create_institution_obj()
        self.create_manufacturer_obj()
        self.create_platform_type_objs()
        self.create_platform_objs()
        self.create_instrument_objs()
        self.create_instrument_on_platform_objs()
        self.create_deployments_objs()
        self.create_sensors()

    def test_model_to_dict_simple(self):
        all_names = get_apps_model_name()
        print(all_names)

    def test_convert_model_to_dict_simple(self):
        instrument_on_platform_objs = get_instrument_on_platform_by_platform("cabot")
        instrument_on_platform_obj = instrument_on_platform_objs[0]
        res = convert_model_to_dict_simple(instrument_on_platform_obj)
        self.assertEqual(res, {'start_time': '2017-03-12 12:00:00', 'end_time': None, 'comment': None,
                               'platform': 'cabot', 'instrument': 'c'}
                         )
        platform_obj = get_platform_by_name('cabot')
        res = convert_model_to_dict_simple(platform_obj)
        print(res)

    def test_covert_model_to_dict_recursive(self):
        # test instrument on platform
        instrument_on_platform_objs = get_instrument_on_platform_by_platform("cabot")
        instrument_on_platform_obj = instrument_on_platform_objs[0]
        res = convert_model_to_dict_recursive(instrument_on_platform_obj)
        print(res)
        deployment_obj = get_deployment_by_platform_name_start_time(start_time='2017-03-12 12:00:00',
                                                                    platform_name='cabot')
        # test deployment
        res = convert_model_to_dict_recursive(deployment_obj)
        print(res)
        # test_instrument on platform
        instrument_objs = get_instruments_by_deployment('cabot', "2019-05-12 12:00:00")
        instrument_obj = instrument_objs[0]
        res = convert_model_to_dict_recursive(instrument_obj)
        print(res)
        # test instrument with a master instrument
        instrument_obj = instrument_objs[1]
        res = convert_model_to_dict_recursive(instrument_obj)
        print(res)

        # test_sensor
        sensors = get_sensors_by_platform("cabot")
        sensor = sensors[0]
        res = convert_model_to_dict_recursive(sensor)
        print(res)


class TestCreateInvalidData(TestCase):

    def create_project_obj(self):
        self.project_obj1 = Project.objects.create(name="project_a")
        self.project_obj2 = Project.objects.create(name="project_b")

    def create_institution_obj(self):
        self.organization_objs = {}
        organization = ["OTN", "meopar", "dalhousie"]
        for org in organization:
            obj = Institution.objects.create(name=org)
            self.organization_objs[org] = obj

        return self.organization_objs

    def create_manufacturer_obj(self):
        self.manufacturer_obj = Manufacturer.objects.create(name="ceotr")

    def create_instrument_objs(self):
        self.instrument_obj1 = Instrument.objects.create(identifier="c", short_name="chi", long_name="chi shen me",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj2 = Instrument.objects.create(identifier="d", short_name="he",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj3 = Instrument.objects.create(identifier="e", short_name="wan",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj4 = Instrument.objects.create(identifier="f", short_name="le",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj5 = Instrument.objects.create(identifier="g", short_name="hai",
                                                         manufacturer=self.manufacturer_obj)

    def create_platform_type_objs(self):
        self.platform_type_objs = {}
        platform_types = ["mooring", "profiler", "VOS", "Slocum Glider G3", "Slocum Glider G1", "Slocum Glider G2",
                          "Wave Glider SV2"]
        for t in platform_types:
            obj = PlatformType.objects.create(model=t, manufacturer=self.manufacturer_obj)
            self.platform_type_objs[t] = obj
        return self.platform_type_objs

    def create_platform_objs(self):
        self.platform_obj1 = Platform.objects.create(name="cabot", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G3"])
        self.platform_obj2 = Platform.objects.create(name="scotia", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G3"])
        self.platform_obj3 = Platform.objects.create(name="Fundy", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G2"])
        self.platform_obj4 = Platform.objects.create(name="bond", institution=self.organization_objs["OTN"],
                                                     platform_type=self.platform_type_objs["Slocum Glider G1"])

    def setUp(self):
        self.create_project_obj()
        self.create_institution_obj()
        self.create_manufacturer_obj()
        self.create_platform_type_objs()
        self.create_platform_objs()
        self.create_instrument_objs()

    def test_create_manufacturer(self):
        self.manufacturer_obj1 = Manufacturer.objects.create(name="ceotr")
        self.manufacturer_obj1_1 = Manufacturer.objects.create(name="ceotr")
        self.manufacturer_obj2 = Manufacturer.objects.create(name="CEOTR")

    def test_create_instrument(self):
        # Duplicate instrument
        self.instrument_obj1 = Instrument.objects.create(identifier="c", short_name="chi", long_name="chi shen me",
                                                         manufacturer=self.manufacturer_obj)
        self.instrument_obj2 = Instrument.objects.create(identifier="c", short_name="chi", long_name="chi shen me",
                                                         manufacturer=self.manufacturer_obj)

    def test_create_instrument_on_platform(self):
        # Duplicated Instrument on platform
        self.instrument_on_platform_obj1 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj1,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2017-03-12 12:00:00",
                                                                               end_time="2018-06-12 12:00:00")
        self.instrument_on_platform_obj2 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj1,
                                                                               platform=self.platform_obj1,
                                                                               start_time="2018-05-12 12:00:00",
                                                                               end_time="2018-06-12 12:00:00")
        res = get_instrument_on_platform_by_platform("cabot")
        self.assertEqual(2, len(res))

        # One Instrument one different platform
        self.instrument_on_platform_obj2 = InstrumentOnPlatform.objects.create(instrument=self.instrument_obj1,
                                                                               platform=self.platform_obj2,
                                                                               start_time="2018-05-12 12:00:00",
                                                                               end_time="2018-06-12 12:00:00")
        res2 = get_instrument_on_platform_by_platform("scotia")
        self.assertEqual(1, len(res2))

    def test_create_sensor(self):
        # create duplicate sensor
        self.sensor_obj1 = Sensor.objects.create(instrument=self.instrument_obj1, identifier="identifier1",
                                                 long_name="sensor long name", standard_name="standard name")

        self.sensor_obj2 = Sensor.objects.create(instrument=self.instrument_obj1, identifier="identifier1",
                                                 long_name="sensor long name", standard_name="standard name")
        res = list(Sensor.objects.filter(instrument=self.instrument_obj1))
        self.assertEqual(2, len(res))

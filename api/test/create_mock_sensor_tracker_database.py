import os
import json

MOCK_JSON_FILE_NAME = "mock_database_json"
JSON_DATA_FILES = ["institution", "manufacturer", "project", "platform_type", "platform", "instrument", "power_type",
                   "deployment", "sensor", "instrument_on_platform", "sensor_on_instrument"]


def create_mock_database():
    from general import models as general
    from instruments import models as instruments
    from platforms import models as platforms
    json_dict_list = import_json_contents()
    project_json = json_dict_list["project"]
    for x in project_json:
        general.Project.objects.create(**filter_out_create_day_modified_day(x))

    institution_json = json_dict_list["institution"]
    for x in institution_json:
        general.Institution.objects.create(**filter_out_create_day_modified_day(x))

    manufacturer_json = json_dict_list["manufacturer"]
    for x in manufacturer_json:
        general.Manufacturer.objects.create(**filter_out_create_day_modified_day(x))

    platform_type_json = json_dict_list["platform_type"]
    for x in platform_type_json:
        platforms.PlatformType.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    platform_json = json_dict_list["platform"]
    for x in platform_json:
        platforms.Platform.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    instrument_json = json_dict_list["instrument"]
    for x in instrument_json:
        instruments.Instrument.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    power_type_json = json_dict_list["power_type"]
    for x in power_type_json:
        platforms.PlatformPowerType.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    deployment_json = json_dict_list["deployment"]
    for x in deployment_json:
        platforms.PlatformDeployment.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    sensor_json = json_dict_list["sensor"]
    for x in sensor_json:
        instruments.Sensor.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    instrument_on_platform_json = json_dict_list["instrument_on_platform"]
    for x in instrument_on_platform_json:
        instruments.InstrumentOnPlatform.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    sensor_on_instrument_json = json_dict_list["sensor_on_instrument"]
    for x in sensor_on_instrument_json:
        instruments.SensorOnInstrument.objects.create(**replace_to_id(filter_out_create_day_modified_day(x)))

    return json_dict_list


def import_json_contents():
    current = os.path.dirname(os.path.realpath(__file__))
    json_folder = os.path.join(current, MOCK_JSON_FILE_NAME)
    json_dict = dict()
    for x in JSON_DATA_FILES:
        with open(os.path.join(json_folder, ".".join([x, "json"]))) as f:
            json_dict[x] = json.loads(f.read())["results"]
    return json_dict


def filter_out_create_day_modified_day(the_dict):
    the_dict.pop("the_dict", None)

    the_dict.pop("created_date", None)
    the_dict.pop("modified_date", None)

    return the_dict


def replace_to_id(the_dict):
    for x in JSON_DATA_FILES:
        if x in the_dict:
            the_dict[x + "_id"] = the_dict.pop(x)
    return the_dict

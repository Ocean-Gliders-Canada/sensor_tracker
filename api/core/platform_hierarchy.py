from api.core.qs_getter import GetQuerySetMethod
from instruments.models import Instrument
from platforms.models import Platform


class GetHierarchy:
    @staticmethod
    def get_hierarchy_by_platform_name(platform_name, start_time):
        platforms = Platform.objects.filter(name=platform_name)

        platform_development_obj = GetQuerySetMethod.get_deployments(platform_name=platform_name, start_time=start_time)
        start_time = platform_development_obj.start_time
        end_time = platform_development_obj.end_time
        platform_name = platform_development_obj.platform.name
        instrument_on_platform_qs = GetQuerySetMethod.get_instrument_on_platform_by_platform_and_time(
            platform_name=platform_name, start_time=start_time, end_time=end_time).prefetch_related(
            'platform').prefetch_related('instrument')
        sensor_on_instrument_qs = []
        for ins in instrument_on_platform_qs:
            sensors = GetQuerySetMethod.get_sensor_on_instrument(instrument_identifier=ins.identifier)
            sensor_on_instrument_qs.append(sensors)

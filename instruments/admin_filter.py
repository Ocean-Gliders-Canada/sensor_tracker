from django.contrib import admin
from platforms.models import PlatformType, Platform

from .models import (
    Instrument,
    InstrumentOnPlatform,
)

from api.core.qs_getter import GetQuerySetMethod


def platform_list_order_by_active():
    list_of_platform_name = []
    queryset = Platform.objects.all().order_by('-active')
    for platform_obj in queryset:
        join_list = [x for x in [platform_obj.name, platform_obj.serial_number] if
                     x is not None]
        list_of_platform_name.append(
            (platform_obj.name,
             "-".join(join_list))
        )
    return list_of_platform_name


def platform_type_list_ordered():
    list_of_platform_types = []
    queryset = PlatformType.objects.all().prefetch_related('manufacturer')
    for platform_type in queryset:
        list_of_platform_types.append(
            (str(platform_type.id), platform_type.model + "-" + platform_type.manufacturer.name)
        )
    return sorted(list_of_platform_types, key=lambda tp: tp[1])


def instrument_list():
    list_of_instruments = []
    queryset = Instrument.objects.all()
    for instrument_obj in queryset:
        join_list = [x for x in [instrument_obj.identifier, instrument_obj.short_name, instrument_obj.serial] if
                     x is not None]
        list_of_instruments.append(
            (instrument_obj.identifier,
             "-".join(join_list))
        )
    return list_of_instruments


# Admin Instrument filters

class InstrumentPlatformTypeFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Type'

    parameter_name = 'platform_type'

    def lookups(self, request, model_admin):
        return platform_type_list_ordered()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """

        if self.value():
            all_relevant_instruments = InstrumentOnPlatform.objects.filter(
                platform__platform_type=self.value()
            ).values()
            relevant_instruments = {}
            for i in all_relevant_instruments:
                if i['instrument_id'] not in relevant_instruments:
                    relevant_instruments[i['instrument_id']] = i
                elif relevant_instruments[i['instrument_id']]['end_time'] is None:
                    pass
                elif i['end_time'] is None:
                    relevant_instruments[i['instrument_id']] = i
                elif i['end_time'] > relevant_instruments[i['instrument_id']]['end_time']:
                    relevant_instruments[i['instrument_id']] = i

            return queryset.filter(pk__in=relevant_instruments.keys())

        else:
            return queryset


class InstrumentPlatformNameFilter(admin.SimpleListFilter):
    title = 'Platform Name'

    parameter_name = 'platform_name'

    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return platform_list_order_by_active()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """

        if self.value():
            return GetQuerySetMethod.get_instrument_by_platform(platform_name=self.value())
        else:
            return queryset


# Instrument On Platform filters

class InstrumentOnPlatformTypeListFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Type'

    parameter_name = 'platform_type'

    def lookups(self, request, model_admin):
        return platform_type_list_ordered()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """

        if self.value() is None:
            return queryset
        else:
            all_relevant_instruments = InstrumentOnPlatform.objects.filter(
                platform__platform_type=self.value()
            ).values()

            relevant_instruments_on_platforms = []

            for r in all_relevant_instruments:
                relevant_instruments_on_platforms.append(r['id'])

            return queryset.filter(pk__in=relevant_instruments_on_platforms)


class InstrumentOnPlatformSortFilter(admin.SimpleListFilter):
    title = 'Sort By'

    parameter_name = 'sort_by'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        sort_ops = [
            ('instrument__identifier', 'Instrument Identifier'),
            ('instrument__short_name', 'Instrument Short Name'),
            ('instrument__long_name', 'Instrument Long Name'),
            ('instrument__modified_date', 'Instrument Date Modified'),
            ('platform__name', 'Platform Name'),
            ('platform__purchase_date', 'Platform Purchase Date'),
        ]
        return sort_ops

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            return queryset.order_by(self.value())


class InstrumentOnPlatformInstrumentIdentifierFilter(admin.SimpleListFilter):
    """
    """
    title = 'Instrument Identifier'

    parameter_name = 'instrument_identifier'

    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        return instrument_list()

    def queryset(self, request, queryset):

        if self.value() is None:
            return queryset
        else:
            return GetQuerySetMethod._get_instrument_on_platform(identifier=self.value())


class InstrumentOnPlatformPlatformNameFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Name'

    parameter_name = 'platform_name'

    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        return platform_list_order_by_active()

    def queryset(self, request, queryset):

        if self.value() is None:
            return queryset
        else:
            return GetQuerySetMethod.get_instrument_on_platform_by_platform(platform_name=self.value())


# Sensor filters


class SensorPlatformNameFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Name'

    parameter_name = 'platform_name'

    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return platform_list_order_by_active()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            queryset = GetQuerySetMethod.get_sensors(..., platform_name=self.value())

            return queryset


class SensorInstrumentIdentifierFilter(admin.SimpleListFilter):
    """
    """
    title = 'Instrument Identifier'

    parameter_name = 'instrument_identifier'

    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        return instrument_list()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            queryset = GetQuerySetMethod.get_sensors(..., instrument_identifier=self.value())

            return queryset

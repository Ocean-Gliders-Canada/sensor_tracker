from django.db.models import Q
from django.contrib import admin
from platforms.models import PlatformType, Platform

from .models import (
    Instrument,
    InstrumentOnPlatform,
    SensorOnInstrument,
)
from django.contrib.admin.filters import (
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter, RelatedOnlyFieldListFilter
)
from api.core.qs_getter import GetQuerySetMethod


# Admin Instrument

class InstrumentOnPlatformTypeListFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Type'

    parameter_name = 'platform_type'

    default_value = 'All'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        list_of_platform_types = []
        queryset = PlatformType.objects.all()
        for platform_type in queryset:
            list_of_platform_types.append(
                (str(platform_type.id), platform_type.model)
            )
        return sorted(list_of_platform_types, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                all_relevant_instruments = InstrumentOnPlatform.objects.filter(
                    platform__platform_type=self.value()
                ).values()

                relevant_instruments_on_platforms = []

                for r in all_relevant_instruments:
                    relevant_instruments_on_platforms.append(r['id'])

                return queryset.filter(pk__in=relevant_instruments_on_platforms)

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(InstrumentOnPlatformTypeListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class InstrumentOnPlatformSortFilter(admin.SimpleListFilter):
    title = 'Sort By'

    parameter_name = 'sort_by'

    default_value = 'All'

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
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.order_by(self.value())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(InstrumentOnPlatformSortFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class InstrumentPlatformTypeFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Type'

    parameter_name = 'platform_type'

    default_value = 'All'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        list_of_platform_types = []
        queryset = PlatformType.objects.all()
        for platform_type in queryset:
            list_of_platform_types.append(
                (str(platform_type.id), platform_type.model + "-" + platform_type.manufacturer.name)
            )
        return sorted(list_of_platform_types, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
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

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(InstrumentPlatformTypeFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class InstrumentIdentifierFilter(admin.SimpleListFilter):
    """
    """
    title = 'Identifier'

    parameter_name = 'identifier'

    default_value = 'All'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        list_of_platform_types = []
        queryset = Instrument.objects.all()
        for instrument in queryset:
            temp = (instrument.identifier, instrument.identifier)
            if temp not in list_of_platform_types:
                list_of_platform_types.append(
                    temp
                )
        return sorted(list_of_platform_types, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                all_relevant_instruments = Instrument.objects.filter(
                    identifier=self.value()
                ).values()
                relevant_instruments = {}
                for i in all_relevant_instruments:
                    if i['id'] not in relevant_instruments:
                        relevant_instruments[i['id']] = i
                    elif i['modified_date'] > relevant_instruments[i['id']]['modified_date']:
                        relevant_instruments[i['instrument_id']] = i
                        # elif i['end_time'] is None:
                        #     relevant_instruments[i['instrument_id']] = i

                return queryset.filter(pk__in=relevant_instruments.keys())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(InstrumentIdentifierFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


# Sensor filters
class SensorInstrumentIdentifierFilter(admin.SimpleListFilter):
    """
    """
    title = 'Instrument'

    parameter_name = 'instrument_identifier'

    default_value = 'All'
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        list_of_platform_types = []
        queryset = Instrument.objects.all()
        for instrument_obj in queryset:
            join_list = [x for x in [instrument_obj.identifier, instrument_obj.short_name, instrument_obj.serial] if
                         x is not None]
            list_of_platform_types.append(
                (instrument_obj.identifier,
                 "-".join(join_list))
            )
        return list_of_platform_types

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            all_relevant_instruments = SensorOnInstrument.objects.filter(
                instrument__identifier=self.value()
            ).values()
            relevant_instrument_ids = []
            for i in all_relevant_instruments:
                relevant_instrument_ids.append(i['id'])

            return queryset.filter(pk__in=relevant_instrument_ids)


class SensorPlatformNameFilter(admin.SimpleListFilter):
    """
    """
    title = 'platform_name'

    parameter_name = 'platform_name'

    default_value = 'All'
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
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

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            queryset = GetQuerySetMethod.get_sensors(..., platform_name=self.value())

            return queryset

    def value(self):
        """
        Return the value (in string format) provided in the request's
        query string for this filter, if any, or None if the value wasn't
        provided.
        """
        return self.used_parameters.get(self.parameter_name)


class SensorAttachedToInstrumentFilter(admin.SimpleListFilter):
    title = 'attached on instrument'
    parameter_name = 'sensor_attached_to_instrument'
    default_value = '0'
    ATTACHED = '1'
    NO_ATTACHED = '2'

    def lookups(self, request, model_admin):
        return (
            (self.ATTACHED, u'Attached on a instrument'),
            (self.NO_ATTACHED, u'No attached on instrument')
        )

    def queryset(self, request, queryset):

        the_value = self.value()
        if the_value is None:
            return queryset

        all_sensor_on_instrument_qs = SensorOnInstrument.objects.filter(end_time=None).prefetch_related('instrument')
        no_repeat_set = {}
        for obj in all_sensor_on_instrument_qs:
            no_repeat_set[obj.instrument.id] = None
        the_keys = no_repeat_set.keys()
        if the_value == self.ATTACHED:
            queryset = queryset.filter(pk__in=the_keys)

        if the_value == self.NO_ATTACHED:
            queryset = queryset.filter(~Q(id__in=the_keys))

        return queryset

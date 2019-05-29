from django.contrib import admin
from django.forms import ModelForm, CharField
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Instrument,
    InstrumentComment,
    InstrumentOnPlatform,
    Sensor
)

from platforms.models import PlatformType, Platform
from django_admin_listfilter_dropdown.filters import DropdownFilter


class InstrumentOnPlatformForm(ModelForm):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


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


class InstrumentOnPlatformAdmin(admin.ModelAdmin):
    form = InstrumentOnPlatformForm
    list_filter = (
        InstrumentOnPlatformTypeListFilter,
        ('platform__name', DropdownFilter),
        ('instrument__identifier', DropdownFilter),
        InstrumentOnPlatformSortFilter)
    list_display = ('instrument', 'platform', 'start_time', 'end_time', 'comment')


admin.site.register(InstrumentOnPlatform, InstrumentOnPlatformAdmin)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    search_fields = ['identifier', 'long_name', 'standard_name', 'instrument__short_name', 'instrument__long_name',
                     'instrument__serial']
    readonly_fields = ('created_date', 'modified_date')
    list_display = ('identifier', 'long_name', 'standard_name', 'instrument', 'include_in_output', 'created_date',
                    'modified_date')
    list_filter = ('include_in_output',)


class SensorInline(admin.StackedInline):
    readonly_fields = ('created_date', 'modified_date')
    model = Sensor
    extra = 0


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


class InstrumentForm(ModelForm):

    class Meta:
        model = Instrument
        fields = '__all__'


class PlatformInline(admin.StackedInline):
    model = InstrumentOnPlatform

    exclude = ["comment"]
    readonly_fields = ["platform", "start_time", "end_time"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date')
    inlines = [PlatformInline,
               SensorInline,
               ]
    list_filter = (InstrumentPlatformTypeFilter,
                   ('identifier', DropdownFilter))
    search_fields = ['identifier', 'short_name', 'long_name', 'serial', 'manufacturer__name']
    list_display = ('identifier', 'short_name', 'long_name', 'serial', 'manufacturer', 'created_date', 'modified_date')
    form = InstrumentForm


@admin.register(InstrumentComment)
class InstrumentCommentAdmin(admin.ModelAdmin):
    list_display = ('instrument', 'created_date', 'short_comment')

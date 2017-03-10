from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Instrument,
    InstrumentComment,
    InstrumentOnPlatform,
    Sensor
)

from platforms.models import PlatformType


class InstrumentOnPlatformForm(ModelForm):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


class InstrumentOnPlatformAdmin(ModelAdmin):
    form = InstrumentOnPlatformForm
admin.site.register(InstrumentOnPlatform, InstrumentOnPlatformAdmin)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    pass


class SensorInline(admin.StackedInline):
    model = Sensor
    extra = 0


class InstrumentListFilter(admin.SimpleListFilter):
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
                    elif i['end_time'] > relevant_instruments[i['instrument_id']]['end_time']:
                        relevant_instruments[i['instrument_id']] = i
                    elif i['end_time'] is None:
                        relevant_instruments[i['instrument_id']] = i

                return queryset.filter(pk__in=relevant_instruments.keys())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(InstrumentListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    inlines = [
        SensorInline,
    ]
    list_filter = (InstrumentListFilter, )
    pass


@admin.register(InstrumentComment)
class InstrumentCommentAdmin(admin.ModelAdmin):
    pass

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


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    inlines = [
        SensorInline,
    ]
    pass


@admin.register(InstrumentComment)
class InstrumentCommentAdmin(admin.ModelAdmin):
    pass

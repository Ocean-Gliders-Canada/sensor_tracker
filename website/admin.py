from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Institution,
    PlatformType,
    Platform,
    Instrument,
    InstrumentOnPlatform,
    PlatformDeployment,
    Sensor,
)


# Register your models here.
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass


@admin.register(PlatformType)
class PlatformTypeAdmin(admin.ModelAdmin):
    pass


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'
        widgets = {
            'purchase_date': SuitSplitDateTimeWidget
        }


class PlatformAdmin(ModelAdmin):
    form = PlatformForm
admin.site.register(Platform, PlatformAdmin)


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


class PlatformDeploymentForm(ModelForm):
    class Meta:
        model = PlatformDeployment
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


class PlatformDeploymentAdmin(ModelAdmin):
    form = PlatformDeploymentForm
admin.site.register(PlatformDeployment, PlatformDeploymentAdmin)


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

import warnings

from django.contrib import admin
from django.forms import ModelForm
from django import forms
from datetime import datetime
from django.db.models import Q

from django.core.exceptions import ObjectDoesNotExist
from instruments.admin_filter import (
    SensorOnInstrumentPlatformFilter,
)

from suit.widgets import SuitSplitDateTimeWidget

from instruments.admin_filter import (
    InstrumentPlatformNameFilter,
    InstrumentOnPlatformSortFilter,
    InstrumentOnPlatformTypeListFilter,
    InstrumentPlatformTypeFilter,
    InstrumentOnPlatformInstrumentIdentifierFilter,
    InstrumentOnPlatformPlatformNameFilter,
    SensorInstrumentIdentifierFilter,
    SensorPlatformNameFilter,
)

from .models import (
    Instrument,
    InstrumentOnPlatform,
    Sensor,
    InstrumentCommentBox,
    InstrumentComment,
    SensorOnInstrument,
)

from django.urls import reverse

from platforms.models import Platform


class InstrumentOnPlatformForm(ModelForm):
    class Meta:
        model = InstrumentOnPlatform
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


class InstrumentOnPlatformAdmin(admin.ModelAdmin):
    form = InstrumentOnPlatformForm
    list_filter = (
        InstrumentOnPlatformTypeListFilter,
        InstrumentOnPlatformPlatformNameFilter,
        InstrumentOnPlatformInstrumentIdentifierFilter,
        InstrumentOnPlatformSortFilter
    )

    list_display = (
        'instrument_identifier', 'instrument_serial', 'instrument_short_name', 'instrument_long_name', 'platform',
        'start_time', 'end_time', 'comment')
    readonly_fields = ('created_date', 'modified_date',)

    def instrument_identifier(self, instance):
        return instance.instrument.identifier

    def instrument_long_name(self, instance):
        return instance.instrument.long_name

    def instrument_short_name(self, instance):
        return instance.instrument.short_name

    def instrument_serial(self, instance):
        return instance.instrument.serial


admin.site.register(InstrumentOnPlatform, InstrumentOnPlatformAdmin)


class SensorForm(ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        include_in_output = cleaned_data.get("include_in_output")
        long_name = cleaned_data.get("long_name")

        if include_in_output and not long_name:
            # Only do something if both fields are valid so far.

            raise forms.ValidationError(
                "Long name must be given when included in output checked"
            )


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    form = SensorForm
    search_fields = ['identifier', 'long_name', 'standard_name']
    readonly_fields = ('created_date', 'modified_date')
    list_display = ('identifier', 'long_name', 'standard_name', 'include_in_output', 'created_date',
                    'modified_date')
    list_filter = (
        'include_in_output',
        SensorPlatformNameFilter,
        SensorInstrumentIdentifierFilter,
    )

    def save_model(self, request, obj, form, change):
        time = datetime.now()
        if not change:
            super().save_model(request, obj, form, change)
            if obj.instrument:
                SensorOnInstrument.objects.create(sensor=obj, instrument=obj.instrument, start_time=time)
        else:
            current_sensor_obj = Sensor.objects.get(id=obj.id)
            current_attched_instrument = current_sensor_obj.instrument
            soi_qs_count = SensorOnInstrument.objects.filter(sensor=obj, instrument=current_attched_instrument).count()
            if current_attched_instrument != obj.instrument:
                if soi_qs_count == 0:
                    if obj.instrument:
                        SensorOnInstrument.objects.create(sensor=obj, instrument=obj.instrument,
                                                          start_time=time,
                                                          end_time=None)
                else:
                    try:
                        the_soi_c = SensorOnInstrument.objects.get(sensor=obj, instrument=current_attched_instrument,
                                                                   end_time=None)
                        the_soi_c.end_time = time
                        the_soi_c.save()
                    except ObjectDoesNotExist as e:
                        warnings.warn("Possible data flaw\n{}".format(e))
                    if obj.instrument is not None:
                        SensorOnInstrument.objects.create(sensor=obj, instrument=obj.instrument,
                                                          start_time=time,
                                                          end_time=None)

            super().save_model(request, obj, form, change)


class InstrumentForm(ModelForm):
    class Meta:
        model = Instrument
        fields = '__all__'


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class PlatformInline(admin.StackedInline):
    model = InstrumentOnPlatform

    exclude = ["comment"]
    readonly_fields = ["platform", "start_time", "end_time"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('instrument').prefetch_related('platform')
        return qs

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class InstrumentOnPlatformDisplayItem:
    def __init__(self, instance):
        self.instrument_on_platform_instance = instance


class SensorOnInstrumentInline(admin.StackedInline):
    model = Sensor
    min_num = 0


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date')

    list_filter = (InstrumentPlatformTypeFilter,
                   InstrumentPlatformNameFilter)

    search_fields = ['identifier', 'short_name', 'long_name', 'serial', 'manufacturer__name']
    list_display = ('identifier', 'short_name', 'long_name', 'serial', 'manufacturer', 'created_date', 'modified_date')
    form = InstrumentForm
    change_form_template = 'admin/custom_change_form.html'
    list_per_page = 40

    def get_queryset(self, request):
        qs = super(InstrumentAdmin, self).get_queryset(request)
        qs = qs.prefetch_related('manufacturer')
        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):
        instrument_obj = Instrument.objects.get(id=int(object_id))
        instrument_on_platform_qs = InstrumentOnPlatform.objects.filter(instrument=instrument_obj).order_by(
            'start_time').prefetch_related('platform')
        objs = list(instrument_on_platform_qs)
        for obj in objs:
            obj.url_edit_link = make_edit_link(obj)
            obj.url_platform_change = make_edit_link(obj.platform)
        sensor_on_instrument = SensorOnInstrument.objects.filter(instrument=instrument_obj)
        sensor_on_instrument = sensor_on_instrument.prefetch_related('sensor').prefetch_related('instrument')

        sensor_obj_set = []
        for soi in sensor_on_instrument:
            soi.url_edit_link = make_edit_link(soi)
            soi.url_sensor_cahnge = make_edit_link(soi.sensor)
            sensor_obj_set.append(soi)

        extra_context = {
            "extra_content": objs,
            "inline_content": sensor_obj_set
        }
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)


def make_edit_link(instance):
    opt = instance._meta
    link = reverse('admin:{}_{}_change'.format(opt.app_label, opt.model_name), args=(instance.id,))
    return link


class SensorOnInstrumentForm(ModelForm):
    class Meta:
        model = SensorOnInstrument
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        instrument = cleaned_data.get("instrument")
        sensor = cleaned_data.get("sensor")
        soi_qs = SensorOnInstrument.objects.filter(instrument=instrument, sensor=sensor, end_time=None)
        if hasattr(self, 'instrance'):
            self_id = self.instrument.id
            soi_qs = soi_qs.filter(~Q(id=self_id))
        if soi_qs.count() != 0:
            raise forms.ValidationError(
                "Must put end time for exist {} {} sensor on instrument table before creating a new one.".format(
                    instrument.identifier, sensor.identifier)
            )


@admin.register(SensorOnInstrument)
class SensorOnInstrumentAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'instrument', 'start_time', 'end_time')
    list_filter = (
        SensorOnInstrumentPlatformFilter,
    )
    form = SensorOnInstrumentForm
    readonly_fields = ('sensor', 'instrument')

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('instrument').prefetch_related('sensor')

        return qs

    def has_add_permission(self, request):
        return False

    def save_model(self, request, obj, form, change):
        if change:
            current_sensor_on_instrument_obj = SensorOnInstrument.objects.get(id=obj.id)
            c_end_time = current_sensor_on_instrument_obj.end_time

            end_time = obj.end_time
            if c_end_time != end_time:
                if c_end_time is None:
                    obj.sensor.instrument = None
                    obj.sensor.save()
                else:
                    if obj.sensor.instrument is not None:
                        raise forms.ValidationError(
                            "Must put end time for exist {} {} sensor on instrument table before creating a new one.".format(
                                obj.instrument.identifier, obj.sensor.identifier)
                        )
                    else:
                        obj.sensor.instrument = obj.instrument
                        obj.sensor.save()

        super().save_model(request, obj, form, change)


class InstrumentCommentBoxInline(admin.TabularInline):
    model = InstrumentComment
    extra = 0
    readonly_fields = ('user', 'created_date', 'modified_date')

    fields = ('user', 'created_date', 'modified_date', 'comment')


class InstrumentCommentBoxForm(ModelForm):
    class Meta:
        model = InstrumentCommentBox
        fields = ('instrument',)


class InstrumentCommentBoxAdmin(admin.ModelAdmin):
    form = InstrumentCommentBoxForm
    inlines = [
        InstrumentCommentBoxInline
    ]
    list_display = ('instrument_identifier', 'instrument_short_name', 'instrument_serial', 'on_platform')
    search_fields = ['instrument__identifier', 'instrument__short_name', 'instrument__long_name',
                     'instrument__serial']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user = request.user

        formset.save()

    def get_queryset(self, request):
        qs = super(InstrumentCommentBoxAdmin, self).get_queryset(request)
        qs = qs.prefetch_related('instrument')
        return qs

    def instrument_identifier(self, instance):
        return instance.instrument.identifier

    def instrument_short_name(self, instance):
        return instance.instrument.short_name

    def instrument_serial(self, instance):
        return instance.instrument.serial

    def on_platform(self, instance):
        platform_obj_queryset = InstrumentOnPlatform.objects.filter(instrument=instance.instrument).select_related(
            'platform')
        platform_names = []
        for o in platform_obj_queryset:
            if not o.end_time:
                platform_names.append(o.platform.name)
        if not platform_names:
            return '-'
        else:
            return " and ".join(platform_names)


admin.site.register(InstrumentCommentBox, InstrumentCommentBoxAdmin)

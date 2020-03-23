import warnings

from django.contrib import admin
from custom_admin import admin as custom_admin_site
from django import forms
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from instruments.admin_filter import (
    SensorOnInstrumentPlatformFilter,
)

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

from common.admin_common import CommentBoxAdminBase
from common.utilities import make_edit_link, make_add_link
from instruments.model_form import (
    InstrumentOnPlatformForm,
    SensorForm,
    InstrumentForm,
    SensorOnInstrumentForm,
    InstrumentCommentBoxForm
)
from common.admin_common import BaseCommentBoxInline


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


custom_admin_site.site.register(InstrumentOnPlatform, InstrumentOnPlatformAdmin)


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
    change_form_template = 'admin/custom_sensor_change_form.html'
    change_list_template = 'admin/custom_change_list.html'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        sensor_obj = Sensor.objects.get(id=int(object_id))
        instrument_on_platform_qs = SensorOnInstrument.objects.filter(sensor=sensor_obj).order_by(
            'start_time').prefetch_related('instrument').prefetch_related('sensor')
        objs = list(instrument_on_platform_qs)
        for obj in objs:
            obj.url_edit_link = make_edit_link(obj)
            obj.url_instrument_change = make_edit_link(obj.instrument)

        sensor_on_instrument_add_link = make_add_link(SensorOnInstrument)
        extra_context = {
            "extra_content": objs,
            "sensor_on_instrument_add_link": sensor_on_instrument_add_link,
        }
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)

    def delete_queryset(self, request, queryset):
        super().delete_queryset(request, queryset)

    def delete_model(self, request, queryset):
        super().delete_model(request, queryset)

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


custom_admin_site.site.register(Sensor, SensorAdmin)


class InstrumentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date')

    list_filter = (InstrumentPlatformTypeFilter,
                   InstrumentPlatformNameFilter)

    search_fields = ['identifier', 'short_name', 'long_name', 'serial', 'manufacturer__name']
    list_display = ('identifier', 'short_name', 'long_name', 'serial', 'manufacturer', 'created_date', 'modified_date')
    form = InstrumentForm
    change_form_template = 'admin/custom_instrument_change_form.html'
    change_list_template = 'admin/custom_change_list.html'
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
        instrument_on_platform_add_link = make_add_link(InstrumentOnPlatform)
        sensor_on_instrument_add_link = make_add_link(SensorOnInstrument)
        extra_context = {
            "extra_content": objs,
            "inline_content": sensor_obj_set,
            "instrument_on_platform_add_link": instrument_on_platform_add_link,
            "sensor_on_instrument_add_link": sensor_on_instrument_add_link,
        }
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)


custom_admin_site.site.register(Instrument, InstrumentAdmin)


class SensorOnInstrumentAdmin(admin.ModelAdmin):
    list_display = ('sensor', 'instrument', 'start_time', 'end_time')
    list_filter = (
        SensorOnInstrumentPlatformFilter,
    )
    form = SensorOnInstrumentForm

    def get_queryset(self, request):
        qs = super().get_queryset(request).prefetch_related('instrument').prefetch_related('sensor')

        return qs

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


custom_admin_site.site.register(SensorOnInstrument, SensorOnInstrumentAdmin)


class InstrumentCommentBoxInline(BaseCommentBoxInline):
    model = InstrumentComment


class InstrumentCommentBoxAdmin(CommentBoxAdminBase):
    form = InstrumentCommentBoxForm
    inlines = [
        InstrumentCommentBoxInline
    ]
    list_display = ('instrument_identifier', 'instrument_short_name', 'instrument_serial', 'on_platform')
    search_fields = ['instrument__identifier', 'instrument__short_name', 'instrument__long_name',
                     'instrument__serial']

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


custom_admin_site.site.register(InstrumentCommentBox, InstrumentCommentBoxAdmin)

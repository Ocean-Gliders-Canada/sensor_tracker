from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitSplitDateTimeWidget
from django_admin_listfilter_dropdown.filters import DropdownFilter

from .models import (
    Instrument,
    InstrumentOnPlatform,
    Sensor,
    InstrumentCommentBox,
    InstrumentComment,
    SensorOnInstrument,
)

from platforms.models import PlatformType, Platform


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
    """
    """
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
    readonly_fields = ('created_date', 'modified_date',)


admin.site.register(InstrumentOnPlatform, InstrumentOnPlatformAdmin)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    search_fields = ['identifier', 'long_name', 'standard_name']
    readonly_fields = ('created_date', 'modified_date')
    list_display = ('identifier', 'long_name', 'standard_name', 'include_in_output', 'created_date',
                    'modified_date')
    list_filter = ('include_in_output',)


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
                   ('identifier', DropdownFilter))
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

        sensor_on_instrument = SensorOnInstrument.objects.filter(instrument=instrument_obj)
        sensor_on_instrument = sensor_on_instrument.prefetch_related('sensor').prefetch_related('instrument')

        sensor_obj_set = []
        for soi in sensor_on_instrument:
            soi.url_edit_link = make_edit_link(soi)
            sensor_obj_set.append(soi)

        extra_context = {
            "extra_content": objs,
            "inline_content": sensor_obj_set
        }
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)


def make_edit_link(instance):
    opt = instance._meta
    link_format = "/admin/{app}/{model}/{instance_id}/change"
    link = link_format.format(app=opt.app_label, model=opt.model_name, instance_id=instance.id)
    return link


@admin.register(SensorOnInstrument)
class SensorOnInstrumentAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs

    def has_module_permission(self, request):
        return False


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

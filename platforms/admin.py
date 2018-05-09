from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from django.db.models import Q
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    PlatformType,
    Platform,
    PlatformComment,
    PlatformDeployment,
    PlatformDeploymentCommentBox,
    PlatformDeploymentComment,
    PlatformPowerType,
    PlatformCommentBox
)


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


class PlatformListFilter(admin.SimpleListFilter):
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
                return queryset.filter(platform_type__id=self.value())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(PlatformListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class PlatformDeploymentListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform__platform_type__id=self.value())


class PlatformDeploymentCommentBoxListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform_deployment__platform__platform_type__id=self.value())


class PlatformAdmin(ModelAdmin):
    form = PlatformForm
    list_filter = (PlatformListFilter,)
    search_fields = ['name', 'serial_number']


admin.site.register(Platform, PlatformAdmin)


class PlatformCommentBoxListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform__platform_type__id=self.value())


class PlatformCommentBoxInline(admin.TabularInline):
    model = PlatformComment
    extra = 0
    readonly_fields = ('user', 'created_date',)

    fields = ('user', 'created_date', 'comment',)


class PlatformCommentForm(ModelForm):
    class Meta:
        fields = '__all__'


class PlatformCommentAdmin(admin.ModelAdmin):
    form = PlatformCommentForm
    inlines = (
        PlatformCommentBoxInline,
    )
    list_filter = (PlatformCommentBoxListFilter,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()


admin.site.register(PlatformCommentBox, PlatformCommentAdmin)


class PlatformDeploymentForm(ModelForm):
    class Meta:
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


class PlatformDeploymentAdmin(ModelAdmin):
    form = PlatformDeploymentForm
    search_fields = ['title', 'deployment_number']
    readonly_fields = ['platform_name']
    list_filter = (PlatformDeploymentListFilter,)

    def save_model(self, request, obj, form, change):
        platformname = obj.platform.name
        obj.platform_name = platformname
        obj.save()


admin.site.register(PlatformDeployment, PlatformDeploymentAdmin)


class PlatformDeploymentCommentBoxInline(admin.TabularInline):
    model = PlatformDeploymentComment
    extra = 0
    readonly_fields = ('user', 'created_date',)

    fields = ('user', 'created_date', 'comment',)


class PlatformDeploymentCommentBoxForm(ModelForm):
    class Meta:
        model = PlatformDeploymentCommentBox
        fields = ('platform_deployment',)

    def __init__(self, *args, **kwargs):
        all_deployment_comment_box_value_list = PlatformDeploymentCommentBox.objects.values_list(
            'platform_deployment_id',
            flat=True)
        if 'instance' in kwargs:
            current_object = kwargs['instance']
        else:
            current_object = None
        if current_object and hasattr(current_object,'platform_deployment_id'):
            current_object_id = current_object.platform_deployment_id
            query_not_include = all_deployment_comment_box_value_list.exclude(platform_deployment_id=current_object_id)
        else:
            query_not_include = all_deployment_comment_box_value_list
        self.commentgroups = PlatformDeployment.objects.filter(Q(platform__platform_type__model="Wave Glider SV2") | Q(
            platform__platform_type__model="Slocum Glider G2") | Q(
            platform__platform_type__model="Slocum Glider G1")).order_by('deployment_number') \
            .exclude(id__in=query_not_include)
        super(PlatformDeploymentCommentBoxForm, self).__init__(*args, **kwargs)
        self.fields['platform_deployment'].queryset = self.commentgroups


class PlatformDeploymentCommentBoxAdmin(ModelAdmin):
    form = PlatformDeploymentCommentBoxForm
    inlines = (
        PlatformDeploymentCommentBoxInline,
    )
    list_filter = (PlatformDeploymentCommentBoxListFilter,)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user

            instance.save()


admin.site.register(PlatformDeploymentCommentBox, PlatformDeploymentCommentBoxAdmin)


@admin.register(PlatformPowerType)
class PlatformPowerTypeAdmin(admin.ModelAdmin):
    pass

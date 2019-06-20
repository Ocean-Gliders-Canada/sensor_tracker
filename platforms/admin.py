import os

from django.contrib import admin
from django.forms import ModelForm
from suit.widgets import SuitSplitDateTimeWidget
from django.db.models import F
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from cgi import escape
from django.utils.encoding import force_unicode

from .models import (
    PlatformType,
    Platform,
    PlatformComment,
    PlatformDeployment,
    PlatformDeploymentCommentBox,
    PlatformDeploymentComment,
    PlatformPowerType,
    PlatformCommentBox,
    DeploymentImage
)


@admin.register(PlatformType)
class PlatformTypeAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer')
    list_filter = ('manufacturer',)
    readonly_fields = ('created_date', 'modified_date',)


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'
        widgets = {
            'purchase_date': SuitSplitDateTimeWidget
        }


class PlatformActiveFilter(admin.SimpleListFilter):
    title = 'active platform'

    parameter_name = 'active'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        return (
            ('0', (u'All')),
            ('1', (u'Yes')),
            ('2', (u'No')),
        )

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() == '0':
            return queryset
        if self.value() == '1':
            return queryset.filter(active=True)
        if self.value() == '2':
            return queryset.filter(active=False)
        return queryset.filter(active=True)


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


class PlatformDeploymentCommentBoxListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform_deployment__platform__platform_type__id=self.value())


class PlatformAdmin(admin.ModelAdmin):
    form = PlatformForm
    list_filter = (PlatformListFilter, PlatformActiveFilter)
    readonly_fields = ('created_date', 'modified_date',)
    search_fields = ['name', 'serial_number']
    list_display = ('name', 'wmo_id', 'serial_number', 'platform_type', 'institution', 'purchase_date')


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
    readonly_fields = ('user', 'created_date', 'modified_date')

    fields = ('user', 'created_date', 'modified_date', 'comment')


class PlatformCommentForm(ModelForm):
    class Meta:
        fields = '__all__'


class PlatformCommentAdmin(admin.ModelAdmin):
    form = PlatformCommentForm
    inlines = (
        PlatformCommentBoxInline,
    )
    list_filter = (PlatformCommentBoxListFilter,)
    list_display = ('platform',)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=True)
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


class PlatformDeploymentHasNumber(admin.SimpleListFilter):
    """
    """
    title = 'Has number'

    parameter_name = 'has_number'

    ops = [
        ('any', 'Any'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    default_value = ops[0]

    def lookups(self, request, model_admin):
        return self.ops

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'yes':
                return queryset.filter(deployment_number__isnull=False)
            elif self.value() == 'no':
                return queryset.filter(deployment_number__isnull=True)
        return queryset

    def value(self):
        value = super(PlatformDeploymentHasNumber, self).value()
        if value is None:
            value = self.default_value
        return str(value)


class ImageFileInput(ClearableFileInput):
    template_with_initial = u'%(initial)s<br /> %(input)s'

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
        }
        template = u'%(input)s'

        input_template = """<input type="file" name="{}" id="{}" />""".format(name, attrs['id'])
        substitutions[
            'input'] = input_template
        if value and hasattr(value, "url"):
            template = self.template_with_initial
            title = value.instance.title
            substitutions['initial'] = (u'<a download="%s" href="%s">%s</a>'
                                        % (escape(title),
                                           escape(value.url),
                                           escape(
                                               force_unicode(os.path.basename(value.url))
                                           )
                                           )
                                        )

        return mark_safe(template % substitutions)


class ImageForm(ModelForm):
    class Meta:
        model = DeploymentImage
        widgets = {
            'picture': ImageFileInput,
        }
        exclude = []


class ImageInline(admin.StackedInline):
    form = ImageForm

    model = DeploymentImage
    fields = ['title', 'image_tag', 'picture', 'created_date', 'modified_date', ]
    readonly_fields = ('image_tag', 'created_date', 'modified_date',)
    extra = 0

    def image_tag(self, obj):
        u = mark_safe('<img src="{url}" width="150" height="150" />'.format(
            url=obj.picture.url))

        return u


class PlatformDeploymentAdmin(admin.ModelAdmin):
    form = PlatformDeploymentForm
    readonly_fields = ('created_date', 'modified_date',)
    search_fields = ['title', 'deployment_number']
    exclude = ('platform_name',)
    list_filter = ('platform__platform_type', 'platform', PlatformDeploymentHasNumber)
    list_display = ('title', 'deployment_number', 'platform', 'start_time', 'end_time', 'sea_name', 'testing_mission')
    inlines = [
        ImageInline,
    ]

    def save_model(self, request, obj, form, change):
        platform_name = obj.platform.name
        obj.platform_name = platform_name
        obj.save()


admin.site.register(PlatformDeployment, PlatformDeploymentAdmin)


class PlatformDeploymentCommentBoxInline(admin.TabularInline):
    model = PlatformDeploymentComment
    extra = 0
    readonly_fields = ('user', 'created_date', 'modified_date')

    fields = ('user', 'created_date', 'modified_date', 'comment')


class PlatformDeploymentCommentBoxForm(ModelForm):
    class Meta:
        model = PlatformDeploymentCommentBox
        fields = ('platform_deployment',)

    def __init__(self, *args, **kwargs):
        super(PlatformDeploymentCommentBoxForm, self).__init__(*args, **kwargs)
        all_deployment_comment_box_value_list = PlatformDeploymentCommentBox.objects.values_list(
            'platform_deployment_id',
            flat=True)
        if 'instance' in kwargs:
            current_object = kwargs['instance']
        else:
            current_object = None
        if current_object and hasattr(current_object, 'platform_deployment_id'):
            current_object_id = current_object.platform_deployment_id
            query_not_include = all_deployment_comment_box_value_list.exclude(platform_deployment_id=current_object_id)
        else:
            query_not_include = all_deployment_comment_box_value_list
        self.commentgroups = PlatformDeployment.objects.order_by(F('deployment_number').desc(nulls_last=True),
                                                                 'title', '-end_time',
                                                                 '-start_time').exclude(id__in=query_not_include)

        self.fields['platform_deployment'].queryset = self.commentgroups


class PlatformDeploymentCommentBoxAdmin(admin.ModelAdmin):
    form = PlatformDeploymentCommentBoxForm
    inlines = (
        PlatformDeploymentCommentBoxInline,
    )
    list_filter = (PlatformDeploymentCommentBoxListFilter,)
    list_display = ('title', 'deployment_number', 'platform', 'start_time', 'end_time')
    search_fields = [
        'platform_deployment__deployment_number',
        'platform_deployment__title',
        'platform_deployment__platform__name'
    ]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.user = request.user

        formset.save()

    def deployment_number(self, instance):
        return instance.platform_deployment.deployment_number

    deployment_number.admin_order_field = 'platform_deployment__deployment_number'

    def title(self, instance):
        return instance.platform_deployment.title

    def platform(self, instance):
        return instance.platform_deployment.platform

    platform.admin_order_field = 'platform_deployment__platform'

    def start_time(self, instance):
        return instance.platform_deployment.start_time

    start_time.admin_order_field = 'platform_deployment__start_time'

    def end_time(self, instance):
        return instance.platform_deployment.end_time

    end_time.admin_order_field = 'platform_deployment__end_time'


admin.site.register(PlatformDeploymentCommentBox, PlatformDeploymentCommentBoxAdmin)


@admin.register(PlatformPowerType)
class PlatformPowerTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date',)

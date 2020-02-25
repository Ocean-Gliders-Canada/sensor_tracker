from custom_admin import admin as custom_admin_site
from django.contrib import admin
from django.utils.safestring import mark_safe

from django_admin_listfilter_dropdown.filters import DropdownFilter
from common.admin_common import BaseCommentBoxInline
from common.admin_common import CommentBoxAdminBase
from instruments.models import InstrumentOnPlatform, SensorOnInstrument
from platforms.models import (
    PlatformType,
    Platform,
    PlatformComment,
    PlatformDeployment,
    PlatformDeploymentCommentBox,
    PlatformDeploymentComment,
    PlatformPowerType,
    PlatformCommentBox,
    DeploymentImage,
)

from common.utilities import (
    make_server_compatibility_relative_url,
    make_edit_link,
    make_add_link
)
from platforms.model_form import (
    PlatformDeploymentForm,
    ImageForm,
    PlatformForm,
    PlatformDeploymentCommentBoxForm,
    PlatformCommentForm
)

from platforms.admin_filter import (
    PlatformListFilter,
    PlatformCommentBoxListFilter,
    PlatformDeploymentHasNumberFilter,
    PlatformActiveFilter,
    PlatformDeploymentCommentBoxListFilter
)


class PlatformTypeAdmin(admin.ModelAdmin):
    list_display = ('model', 'manufacturer')
    list_filter = ('manufacturer',)
    readonly_fields = ('created_date', 'modified_date',)


custom_admin_site.site.register(PlatformType, PlatformTypeAdmin)


class PlatformAdmin(admin.ModelAdmin):
    form = PlatformForm
    list_filter = (
        "platform_type", PlatformActiveFilter,)
    readonly_fields = ('created_date', 'modified_date',)
    search_fields = ['name', 'serial_number']
    list_display = ('name', 'wmo_id', 'serial_number', 'platform_type', 'institution', 'purchase_date')
    change_form_template = 'admin/custom_platform_change_form.html'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    def change_view(self, request, object_id, form_url='', extra_context=None):
        platform_obj = Platform.objects.get(id=int(object_id))
        instrument_on_platform_qs = InstrumentOnPlatform.objects.filter(platform=platform_obj).order_by(
            'start_time').prefetch_related('instrument')
        objs = list(instrument_on_platform_qs)
        for obj in objs:
            obj.url_edit_link = make_edit_link(obj)
            obj.url_instrument_change = make_edit_link(obj.instrument)
        sensor_on_instrument_link = make_add_link(SensorOnInstrument)
        extra_context = {
            "extra_content": objs,
            "instrument_on_platform_add_link": sensor_on_instrument_link,

        }
        return super().change_view(request, object_id, form_url='', extra_context=extra_context)


custom_admin_site.site.register(Platform, PlatformAdmin)


class ImageInline(admin.StackedInline):
    form = ImageForm

    model = DeploymentImage
    fields = ['title', 'image_tag', 'picture', 'created_date', 'modified_date', ]
    readonly_fields = ('image_tag', 'created_date', 'modified_date',)
    extra = 0

    def image_tag(self, obj):
        u = mark_safe('<img src="{url}" width="150" height="150" />'.format(
            url=make_server_compatibility_relative_url(obj.picture.url)))
        return u


class PlatformDeploymentAdmin(admin.ModelAdmin):
    fields = (
        'wmo_id', 'deployment_number', 'platform', 'institution', 'project', 'power_type', 'title',
        ('start_time', 'end_time'),
        ('deployment_latitude', 'recovery_latitude'), ('deployment_longitude', 'recovery_longitude'),
        ('deployment_cruise', 'recovery_cruise'), ('deployment_personnel', 'recovery_personnel'), 'testing_mission',
        'comment', 'acknowledgement', 'contributor_name',
        'contributor_role', 'creator_email', 'creator_name', 'creator_url', 'data_repository_link',
        'publisher_email', 'publisher_name', 'publisher_url', 'metadata_link', 'references', 'sea_name',
        'depth',
    )
    readonly_fields = ('created_date', 'modified_date',)
    search_fields = ['title', 'deployment_number']
    exclude = ('platform_name',)

    list_display = ('title', 'deployment_number', 'platform', 'start_time', 'end_time', 'sea_name', 'testing_mission')
    save_on_top = True

    list_filter = ('platform__platform_type',
                   ('platform__name', DropdownFilter),
                   PlatformDeploymentHasNumberFilter)

    inlines = [
        ImageInline,
    ]

    class Media:
        css = {
            "all": ("custom.css",)
        }


custom_admin_site.site.register(PlatformDeployment, PlatformDeploymentAdmin)


class PlatformPowerTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date',)


custom_admin_site.site.register(PlatformPowerType, PlatformPowerTypeAdmin)


class PlatformCommentBoxInline(BaseCommentBoxInline):
    model = PlatformComment


class PlatformCommentAdmin(CommentBoxAdminBase):
    form = PlatformCommentForm
    inlines = (
        PlatformCommentBoxInline,
    )
    list_filter = (PlatformCommentBoxListFilter,)
    list_display = ('platform',)


custom_admin_site.site.register(PlatformCommentBox, PlatformCommentAdmin)


class PlatformDeploymentCommentBoxInline(BaseCommentBoxInline):
    model = PlatformDeploymentComment


class PlatformDeploymentCommentBoxAdmin(CommentBoxAdminBase):
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.prefetch_related('platform_deployment')
        qs = qs.prefetch_related('platform_deployment__platform')
        return qs

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


custom_admin_site.site.register(PlatformDeploymentCommentBox, PlatformDeploymentCommentBoxAdmin)

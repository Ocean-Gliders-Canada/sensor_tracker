from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin

from suit.widgets import SuitSplitDateTimeWidget



from .models import (
    PlatformType,
    Platform,
    PlatformComment,
    PlatformDeployment,
    PlatformDeploymentComment
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


class PlatformDeploymentListFilter(admin.SimpleListFilter):
    """
    """
    title = 'Platform Type'

    parameter_name = 'platform_type'

    default_value = 'All'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        print(request.GET)
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
                return queryset.filter(platform__platform_type__id=self.value())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(PlatformDeploymentListFilter, self).value()

        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class PlatformAdmin(ModelAdmin):
    form = PlatformForm
    list_filter = (PlatformListFilter, )
    search_fields = ['name','serial_number']
admin.site.register(Platform, PlatformAdmin)


@admin.register(PlatformComment)
class PlatformCommentAdmin(admin.ModelAdmin):
    pass


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
    search_fields = ['title','deployment_number','acknowledgement']
    list_filter = (PlatformDeploymentListFilter, )

admin.site.register(PlatformDeployment, PlatformDeploymentAdmin)


@admin.register(PlatformDeploymentComment)
class PlatformDeploymentCommentAdmin(admin.ModelAdmin):
    pass

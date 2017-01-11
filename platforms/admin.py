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


class PlatformAdmin(ModelAdmin):
    form = PlatformForm
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
admin.site.register(PlatformDeployment, PlatformDeploymentAdmin)


@admin.register(PlatformDeploymentComment)
class PlatformDeploymentCommentAdmin(admin.ModelAdmin):
    pass

import os
from django.db.models import F
from django.forms import ModelForm
from suit.widgets import SuitSplitDateTimeWidget
from django.forms.widgets import ClearableFileInput
from cgi import escape

from .admin import *


class PlatformCommentForm(ModelForm):
    class Meta:
        fields = '__all__'


class PlatformDeploymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PlatformDeploymentForm, self).__init__(*args, **kwargs)
        self.fields['platform'].queryset = Platform.objects.all().order_by('-active')

    class Meta:
        fields = '__all__'
        widgets = {
            'start_time': SuitSplitDateTimeWidget,
            'end_time': SuitSplitDateTimeWidget
        }


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
                                           escape(make_server_compatibility_relative_url(value.url)),
                                           escape(
                                               (os.path.basename(value.url))
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


class PlatformForm(ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'
        widgets = {
            'purchase_date': SuitSplitDateTimeWidget
        }


class PlatformDeploymentCommentBoxForm(ModelForm):
    class Meta:
        model = PlatformDeploymentCommentBox
        fields = ('platform_deployment',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.commentgroups = self.commentgroups.prefetch_related('platform')
        self.fields['platform_deployment'].queryset = self.commentgroups

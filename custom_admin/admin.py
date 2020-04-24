import ast
from django.contrib.auth.models import Group, User, AnonymousUser
from django.contrib.auth.admin import GroupAdmin
from django.contrib.admin import AdminSite
from functools import update_wrapper

from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from rest_framework.authtoken.models import Token
from users.admin import CustomUserAdmin


class TokenView(TemplateView):
    template_name = 'admin/account.html'


class CustomAdminSite(AdminSite):

    def each_context(self, request):
        """
        #todo overwrite it for the new link
        """
        script_name = request.META['SCRIPT_NAME']
        site_url = script_name if self.site_url == '/' and script_name else self.site_url
        user = request.user
        token = "You have no token, please contact site manager to request a account token"
        if user and not isinstance(user, AnonymousUser):
            token_qs = Token.objects.filter(user=user)
            if token_qs.count():
                token = token_qs[0].key

        return {
            'site_title': self.site_title,
            'site_header': self.site_header,
            'site_url': site_url,
            'my_token': token,
            'has_permission': self.has_permission(request),
            'available_apps': self.get_app_list(request),
            'is_popup': False,
        }

    def account(self, request, extra_context=None):
        defaults = {
            'extra_context': {**self.each_context(request), **(extra_context or {})},
        }
        if self.password_change_template is not None:
            defaults['template_name'] = self.password_change_template
        request.current_app = self.name
        return TokenView.as_view(**defaults)(request)

    def get_urls(self):
        from django.urls import include, path, re_path
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            path('', wrap(self.index), name='index'),
            path('login/', self.login, name='login'),
            path('logout/', wrap(self.logout), name='logout'),
            path('password_change/', wrap(self.password_change, cacheable=True), name='password_change'),
            path('account/', wrap(self.account, cacheable=True), name='account'),
            path(
                'password_change/done/',
                wrap(self.password_change_done, cacheable=True),
                name='password_change_done',
            ),
            path('jsi18n/', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            path(
                'r/<int:content_type_id>/<path:object_id>/',
                wrap(contenttype_views.shortcut),
                name='view_on_site',
            ),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                path('%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name='app_list'),
            ]
        return urlpatterns

    def get_model(self, post):
        model_name = post.get('model')[0]
        display_fields = None
        target_model = None
        for _, model_admin in self._registry.items():
            if hasattr(model_admin, "opts"):
                if model_name == model_admin.opts.model_name:
                    display_fields = model_admin.list_display
                    target_model = model_admin.opts.model
                    list_filter = model_admin.list_filter
                    break
        return target_model, model_admin, display_fields, list_filter

    def get_filter_dict(self, key, value):
        PLUS_IN_URL = '%2B'
        SPACE_IN_URL = '+'
        if PLUS_IN_URL in value or SPACE_IN_URL in value:
            new = value.replace(SPACE_IN_URL, ' ')
            new = new.replace(PLUS_IN_URL, '+')
            filter_dict = {key: new}
        else:
            filter_dict = {key: value}
        return filter_dict

    def get_qs(self, request, target_model, model_admin, list_filter, filter_info):
        queryset = target_model.objects.all()
        if filter_info:
            for key in filter_info:
                for item in list_filter:
                    if isinstance(item, str) and item in key:
                        filter_dict = {key: filter_info.get(key)}
                        queryset = queryset.filter(**filter_dict)
                    elif isinstance(item, tuple) and key in item:
                        filter_dict = {key: filter_info.get(key)}
                        queryset = queryset.filter(**filter_dict)
                    elif not isinstance(item, (str, tuple)) and item.parameter_name == key:
                        filter_dict = self.get_filter_dict(key, filter_info.get(key))
                        item = item(request=None, params=filter_dict, model=target_model, model_admin=model_admin)
                        queryset = queryset & item.queryset(request=request, queryset=queryset)
        return queryset

    def get_filter_info(self, post):
        filter_info = post.get('filter')
        filter_info = ast.literal_eval(filter_info)
        return filter_info

    def get_csv(self, display_fields, queryset):
        header = ','.join(display_fields) + '\n'
        lines = []
        for item in queryset:
            line = []
            for field in display_fields:
                value = getattr(item, field)
                if value is None:
                    value = ''
                elif not isinstance(value, str):
                    value = str(value)
                line.append(value)
            line_str = ','.join(line)
            lines.append(line_str)
        data = '\n'.join(lines)
        res_csv = header + data
        return res_csv

    @csrf_exempt
    def download(self, request):
        post = request.POST
        filter_info = self.get_filter_info(post)
        post_dict = dict(post)
        target_model, model_admin, display_fields, list_filter = self.get_model(post_dict)
        if filter_info:
            queryset = self.get_qs(request, target_model, model_admin, list_filter, filter_info)
        else:
            queryset = target_model.objects.all()
        response = StreamingHttpResponse(content_type='text/csv')
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename="model.csv"'
        res_csv = self.get_csv(display_fields, queryset)
        response.streaming_content = res_csv
        return response


site = CustomAdminSite()
site.register(Group, GroupAdmin)
site.register(User, CustomUserAdmin)

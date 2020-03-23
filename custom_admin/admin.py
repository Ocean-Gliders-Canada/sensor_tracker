import codecs
import csv

from django.contrib.auth.models import Group, User, AnonymousUser
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.admin import AdminSite
from functools import update_wrapper

from django.http import HttpResponse, StreamingHttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.views.generic.base import TemplateView
from rest_framework.authtoken.models import Token

from api.core.qs_getter import GetQuerySetMethod
from users.admin import CustomUserAdmin


class TokenView(TemplateView):
    template_name = 'admin/account.html'

class Echo:


    def write(self, value):
        return value

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

    @csrf_exempt
    def download(self, request):
        if True:
            print(request.POST)

        return render_to_response('admin/a.html')
        # response = StreamingHttpResponse(content_type='text/csv')
        # response['Content-'] = "attachment;filename='abc.csv'"
        #
        # rows = ("{},{}\n".format(row, row) for row in range(1, 100000))
        # response.streaming_content = rows
        # # print(type(rows))
        # # response = HttpResponse('success')
        # return response






site = CustomAdminSite()
site.register(Group, GroupAdmin)
site.register(User, CustomUserAdmin)

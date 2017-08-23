from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_deployments/(?P<plat_name>[\w+ ]+)/$', views.get_deployments, name='get_deployments')
]

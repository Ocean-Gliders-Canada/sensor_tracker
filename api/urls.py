from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_deployments/$', views.get_deployments, name='get_deployments')
]

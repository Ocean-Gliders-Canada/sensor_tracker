from django.conf.urls import url

from . import views
from rest_framework.authtoken import views as r_views

urlpatterns = [
    # url(r'^spec/$')
    url(r'^get_deployments/$', views.get_deployments, name='get_deployments'),
    url(r'^get_instruments/$', views.get_instruments, name='get_instruments'),
    url(r'^get_instruments_on_platform/$', views.get_instruments_on_platform, name='get_instruments_on_platform'),
    url(r'^get_sensors/$', views.get_sensors, name='get_sensors'),
    url(r'^get_platform/$', views.get_platform, name='get_platform'),
    url(r'^get_manufacturer/$', views.get_manufacturer, name='get_manufacturer'),
    url(r'^get_institutions/$', views.get_institutions, name='get_institutions'),
    url(r'^get_project/$', views.get_project, name='get_project'),
    url(r'^get_platform_type/$', views.get_platform_type, name='get_platform_type'),
    url(r'^get_platform_deployments/$', views.get_platform_deployments, name='get_platform_deployments'),
    url(r'^get_deployment_instruments/$', views.get_deployment_instruments, name='get_deployment_instruments'),
    url(r'^get_output_sensors/$', views.get_output_sensors, name='get_output_sensors'),
    url(r'^insert_deployment/$', views.insert_deployment, name='insert_deployment'),
    url(r'^insert_platform/$', views.insert_platform, name='insert_platform'),
    url(r'^insert_project/$', views.insert_project, name='insert_project'),
    url(r'^insert_instrument_on_platform/$', views.insert_instrument_on_platform, name='insert_instrument_on_platform'),
    url(r'^insert_platform_type/$', views.insert_platform_type, name='insert_platform_type'),
    url(r'^insert_instrument/$', views.insert_instrument, name='insert_instrument'),
    url(r'^insert_sensor/$', views.insert_sensor, name='insert_sensor'),

]


# 3rd Party Urls
urlpatterns += [
    url(r'^get_token/', r_views.obtain_auth_token)
]

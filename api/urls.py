from django.conf.urls import url

from . import views
from rest_framework.authtoken import views as r_views

urlpatterns = [
    # url(r'^spec/$')
    url(r'^get_deployments/$', views.GetDeploymentByPlatformNameStartTime.get_deployment_by_platform_name_start_time,
        name='get_deployments'),
    url(r'^get_instruments/$', views.GetInstrument.get_instruments, name='get_instruments'),
    url(r'^get_instruments_on_platform/$', views.GetInstrumentOnPlatform.get_instruments_on_platform,
        name='get_instruments_on_platform'),
    url(r'^get_sensors/$', views.GetSensors.get_sensors, name='get_sensors'),
    url(r'^get_platform/$', views.GetPlatform.get_platform, name='get_platform'),
    url(r'^get_manufacturer/$', views.GetManufacturer.get_manufacturer, name='get_manufacturer'),
    url(r'^get_institutions/$', views.GetInstitutions.get_institutions, name='get_institutions'),
    url(r'^get_project/$', views.GetProject.get_project, name='get_project'),
    url(r'^get_platform_type/$', views.get_platform_type, name='get_platform_type'),
    url(r'^get_platform_deployments/$', views.GetPlatformDeployments.get_platform_deployments,
        name='get_platform_deployments'),
    url(r'^get_deployment_instruments/$', views.GetDeploymentInstruments.get_deployment_instruments,
        name='get_deployment_instruments'),
    url(r'^get_sensors_by_platform/$', views.GetSensorsByPlatform.get_sensors_by_platform,
        name='get_sensors_by_platform'),
    url(r'^insert_deployment/$', views.insert_deployment, name='insert_deployment'),
    url(r'^insert_platform/$', views.insert_platform, name='insert_platform'),
    url(r'^insert_project/$', views.insert_project, name='insert_project'),
    url(r'^insert_instrument_on_platform/$', views.insert_instrument_on_platform, name='insert_instrument_on_platform'),
    url(r'^insert_platform_type/$', views.insert_platform_type, name='insert_platform_type'),
    url(r'^insert_instrument/$', views.insert_instrument, name='insert_instrument'),
    url(r'^insert_sensor/$', views.insert_sensor, name='insert_sensor'),
    url(r'^update_component/$', views.update_component, name='update_component'),
    url(r'get_platform_deployment_comments/', views.GetPlatformDeploymentComment.get_platform_deployment_comments,
        name='get_platform_deployment_comments'),
    url(r'get_platform_by_type/', views.GetPlatformByType.get_platform_by_type, name='get_platform_by_type'),
    url(r'get_power/', views.GetPower.get_power, name='get_power'),
    url(r'^spec/$', views.spec, name='spec')

]

# 3rd Party Urls
urlpatterns += [
    url(r'^get_token/', r_views.obtain_auth_token)
]

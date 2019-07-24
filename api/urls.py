from django.conf.urls import url
from django.conf.urls import url, include

from rest_framework import routers
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .core.token_view import obtain_auth_token
from . import views
from.core.router import CustomRouter



schema_view = get_schema_view(
    openapi.Info(
        title="Sensor Tracker API",
        default_version='v2',
        description="API connect to sensor sensor tracker database",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ceotr@ocean.dal.ca"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# 3rd Party Urls
urlpatterns += [
    url(r'^get_token/', obtain_auth_token)
]

router = CustomRouter()


router.register(r'institution', views.GetInstitutions, basename='institution')
router.register(r'project', views.GetProject, basename='project')
router.register(r'manufacturer', views.GetManufacturer, basename='manufacturer')
router.register(r'instrument', views.GetInstrument, basename='instrument')
# instrument_comment
router.register(r'instrument_on_platform', views.GetInstrumentOnPlatform, basename='instrument_on_platform')
router.register(r'sensor_on_instrument', views.GetSensorOnInstrument, basename='sensor_on_instrument')
router.register(r'sensor', views.GetSensor, basename='sensor')
router.register(r'platform_type', views.GetPlatformType, basename='platform_type')
router.register(r'platform', views.GetPlatform, basename='platform')
router.register(r'power', views.GetPower, basename='power')
router.register(r'deployment', views.GetDeployment, basename='deployment')
router.register(r'deployment_comment', views.GetPlatformDeploymentComment, basename='deployment_comment')
router.register(r'platform_comment', views.GetPlatformComment, basename='platform_comment')

urlpatterns += router.urls

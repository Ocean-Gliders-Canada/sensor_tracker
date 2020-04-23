"""sensor_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
# from django.contrib import admin
from custom_admin import admin
from django.conf.urls.static import static

from django.conf import settings
from django.urls import path

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^admin/', admin.site.urls),
                  url(r'^', admin.site.urls),
                  url(r'^api/', include(('api.urls', 'api'), namespace='api')),
                  url(r'^download/*', admin.site.download),
                  path('api-auth/', include('rest_framework.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      # path('__debug__/', include(debug_toolbar.urls)),

                      # For django versions before 2.0:
                      url(r'^__debug__/', include(debug_toolbar.urls)),

                  ] + urlpatterns

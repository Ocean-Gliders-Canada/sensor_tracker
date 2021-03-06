from rest_framework.routers import DefaultRouter
from collections import OrderedDict
from ..views import APIRootView


class CustomRouter(DefaultRouter):

    def get_api_root_view(self, api_urls=None):
        """
        Return a basic root view.
        """
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        return APIRootView.as_view(api_root_dict=api_root_dict)

import copy

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin

from api.core.exceptions import VariableError
from api.core.simple_serializer_factory import serializer_factory
from rest_framework.response import Response


class ApiBaseView(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin):
    # either accept accept option or use default get_method and post method
    accept = []
    accept_option = []
    mutual_exclusion = []
    variable_error_message = ""
    queryset_method = None

    def variable_check(self, the_get):

        # to check if all required variable are here
        for v in self.accept:
            if v not in the_get:
                raise VariableError(self.variable_error_message)

        # to check no given value that should be here
        assign_list = []
        for i in range(len(self.mutual_exclusion)):
            assign_list.append([])

        for index, v_p in enumerate(self.mutual_exclusion):
            if type(v_p) is list:
                for vv_p in v_p:
                    if vv_p in the_get:
                        assign_list[index].append(vv_p)
            else:
                if v_p in the_get:
                    assign_list[index].append(v_p)
        count = 0
        for x in assign_list:
            if len(x) > 0:
                count += 1
        if count > 1:
            raise VariableError(self.variable_error_message)

        return True

    def generate_input_argument(self, the_get):
        input_dict = dict()
        for v in self.accept:
            input_dict[v] = the_get[v]

        for v in self.accept_option:
            if v in the_get:
                input_dict[v] = the_get[v]
        return input_dict

    def initial(self, request, *args, **kwargs):
        # the step before handle the request by handler
        super().initial(request, *args, **kwargs)
        assert self.queryset_method is not None, (
                "'%s' should either include a `queryset_method` attribute, "
                "or override the `get_queryset()` method."
                % self.__class__.__name__
        )
        # create the queryset and enhanced the serializer class
        get_dict = copy.deepcopy(self.request._request.GET)
        depth = get_dict.get("depth", 0)

        def depth_limit(depth):
            if type(depth) is str:
                try:
                    depth = int(depth)
                except Exception:
                    depth = 0
                if depth > 10:
                    depth = 10
                elif depth < 0:
                    depth = 0
            return depth

        depth = depth_limit(depth)
        self.serializer_class = serializer_factory(self.serializer_class, depth)

        if self.variable_check(get_dict):
            kwargs = self.generate_input_argument(get_dict)
            if depth:
                kwargs["depth"] = depth
            else:
                kwargs["depth"] = 0
            qs = self.queryset_method(**kwargs)
            self.queryset = qs

        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method."
                % self.__class__.__name__
        )

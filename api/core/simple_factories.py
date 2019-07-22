from django_filters import rest_framework as filters
from django.db import models

FIELD_TYPE_INDEX = 0
HELP_TEXT_INDEX = 1
MAPPING_RELATION = {

}


def serializer_factory(serializer, depth):
    serializer.Meta.depth = depth

    return serializer


def filterset_class_factory(view_obj):
    # use type to build a class
    serializer_class = getattr(view_obj, "serializer_class", None)
    model = serializer_class.Meta.model

    filterset_class = getattr(view_obj, "filterset_class", None)
    if filterset_class:
        # todo: I am thinking hard about this
        return filterset_class
    else:
        type_arguments = filterset_field_attributes_dict_generator(model, view_obj.accept_basic)
        filterset_class = type(model.__name__ + "_filterset_class", (filters.FilterSet,), type_arguments)
    return filterset_class


def filterset_field_attributes_dict_generator(model, attrs):
    attrs_dict = dict()
    model_concrete_fields = model._meta.concrete_fields
    simplified_fields = generate_name_help_text(model_concrete_fields)
    for x in attrs:
        if x in simplified_fields:
            if simplified_fields[x][FIELD_TYPE_INDEX] == models.CharField:
                help_text = simplified_fields[x][HELP_TEXT_INDEX]
                if not help_text:
                    help_text = attrs.get(x, "")
                attrs_dict[x] = filters.CharFilter(field_name=x, help_text=help_text)
    return attrs_dict


def generate_name_help_text(model_meta_concrete_fields):
    ret_dict = dict()
    for x in model_meta_concrete_fields:
        name = x.name
        if name != 'id':
            ret_dict[name] = (type(x), x.help_text)
    return ret_dict

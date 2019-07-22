from django.contrib.admin.models import LogEntry, ADDITION, ContentType


def query_optimize_decorator(prefetch_related_variables=None):
    # Todo: maybe develop different prefetch_related for different depth level
    def decorator(func):
        def wrapper(*args, **kwargs):
            depth = kwargs.pop("depth", 0)
            qs = func(**kwargs)
            if depth and prefetch_related_variables:
                for x in prefetch_related_variables:
                    qs = qs.prefetch_related(x)

            return qs

        return wrapper

    return decorator


def log_entry_create_decorator(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        res = func(*args, **kwargs)
        serializer = res.data.serializer
        model = serializer.Meta.model
        data = serializer.data
        data_repr = data.__repr__()
        obj_dict = serializer._data
        obj_id = data["id"]
        obj = model(**obj_dict)
        log_obj = LogEntry.objects.log_action(user_id=request.user.id,
                                              content_type_id=ContentType.objects.get_for_model(model).pk,
                                              object_id=obj_id,
                                              object_repr="API added: {}".format(obj.__str__()),
                                              action_flag=ADDITION,
                                              change_message=[{"added": data_repr}])
        del obj
        log_obj.save()
        return res

    return wrapper


def log_entry_update_decorator(func):
    ...

# def log_entry_delete_decorator(func):
#     def wrapper(*args, **kwargs):
#         request = args[1]
#         res = func(*args, **kwargs)
#         serializer = res.data.serializer
#         model = serializer.Meta.model
#         data = serializer.data
#         data_repr = data.__repr__()
#         obj_dict = serializer._data
#         obj_id = data["id"]
#         obj = model(**obj_dict)
#         log_obj = LogEntry.objects.log_action(user_id=request.user.id,
#                                               content_type_id=ContentType.objects.get_for_model(model).pk,
#                                               object_id=obj_id,
#                                               object_repr="API added: {}".format(obj.__str__()),
#                                               action_flag=ADDITION,
#                                               change_message=[{"added": data_repr}])
#         del obj
#         log_obj.save()
#         return res

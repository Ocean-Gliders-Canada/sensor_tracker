from .util import get_all_model_name
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, ContentType


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


def log_entry_create_decorator(action_type="added"):
    allowed_type = ("added", "changed")
    if action_type not in allowed_type:
        raise AttributeError("action type must be in {}".format(allowed_type))

    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[1]
            res = func(*args, **kwargs)
            serializer = res.data.serializer
            model = serializer.Meta.model
            data = serializer.data
            data_repr = data.__repr__()
            obj_dict = serializer._data
            all_model_name = get_all_model_name()

            obj_id = data["id"]
            new_obj_dict = {}
            for key in obj_dict:
                tmp_key = key.replace("_", "")
                if tmp_key in all_model_name:
                    new_obj_dict[key + "_id"] = obj_dict[key]
                else:
                    new_obj_dict[key] = obj_dict[key]
            obj = model(**new_obj_dict)

            if action_type == "added":
                action_flag = ADDITION
                change_message = [{action_type: {action_type: data_repr}}]
            else:
                action_flag = CHANGE
                change_message = [
                    {action_type: {"fields": ["operation by API doesn't support to show the changes yet"]}}]
            log_obj = LogEntry.objects.log_action(user_id=request.user.id,
                                                  content_type_id=ContentType.objects.get_for_model(model).pk,
                                                  object_id=obj_id,
                                                  object_repr="API: {}".format(obj.__str__()),
                                                  action_flag=action_flag,
                                                  change_message=change_message)
            del obj
            log_obj.save()
            return res

        return wrapper

    return decorator

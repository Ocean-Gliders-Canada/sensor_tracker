from rest_framework.mixins import CreateModelMixin

from .decorator import log_entry_create_decorator


class CustomCreateModelMixin(CreateModelMixin):
    """
    Create a model instance.
    """

    @log_entry_create_decorator
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)



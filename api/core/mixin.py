from rest_framework.mixins import CreateModelMixin, UpdateModelMixin

from .decorator import log_entry_create_decorator


class CustomCreateModelMixin(CreateModelMixin):
    """
    Create a model instance.
    """

    @log_entry_create_decorator()
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CustomUpdateModelMixin(UpdateModelMixin):
    """
    Update a model instance
    """

    @log_entry_create_decorator("changed")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @log_entry_create_decorator("changed")
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

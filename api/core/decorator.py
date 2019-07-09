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

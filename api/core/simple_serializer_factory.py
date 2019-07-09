def serializer_factory(serializer, depth):
    serializer.Meta.depth = depth

    return serializer

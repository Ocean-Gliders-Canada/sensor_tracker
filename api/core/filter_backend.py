from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.compat import coreapi, coreschema


class CustomFilterBackend(DjangoFilterBackend):
    def get_filter_parameters(self, view):
        return super().get_coreschema_field(view)

    def get_special_fields(self, view):
        res_fileds = []
        accept_option = view.accept_option
        if accept_option:
            for option, value in accept_option.items():
                res_fileds.append(coreapi.Field(
                    name=option,
                    required=False,
                    location='query',
                    schema=coreschema.String(
                        title=option,
                        description=value
                    )
                ))
        return res_fileds

    def get_schema_fields(self, view):
        res = super().get_schema_fields(view)
        res += self.get_special_fields(view)
        res += generate_default_field()
        return res


def generate_default_field():
    return [
        coreapi.Field(
            name="depth",
            required=False,
            location='query',
            schema=coreschema.Integer(
                title='depth',
                description="The depth option should be set to an integer value that indicates the"
                            " depth of relationships that should be traversed before reverting to a flat representation. "
            )
        ),
        coreapi.Field(
            name="format",
            required=False,
            location='query',
            schema=coreschema.String(
                title='format',
                description="The format of API output"
            )
        )
    ]

from collections import OrderedDict

from rest_framework.metadata import SimpleMetadata


class CustomSimpleMetadata(SimpleMetadata):

    def determine_metadata(self, request, view):
        metadata = OrderedDict()
        metadata['name'] = view.get_view_name()
        metadata['description'] = view.get_view_description()
        metadata['renders'] = [renderer.media_type for renderer in view.renderer_classes]
        metadata['parses'] = [parser.media_type for parser in view.parser_classes]
        description_argument = None
        if hasattr(view, "accept_option"):
            description_argument = {
                "accept_option": getattr(view, "accept_option"),
                "mutual_exclusion": getattr(view, "mutual_exclusion")
            }
        if hasattr(view, 'get_serializer'):
            actions = self.determine_actions(request, view)
            if actions:
                metadata['actions'] = actions
        metadata['argument_description'] = description_argument
        return metadata

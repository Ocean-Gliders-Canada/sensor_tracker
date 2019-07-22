from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import AuthTokenSerializer


class CustomObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        user = vd.get('user', None)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            token_key = token.key
        else:
            token_key = vd.get('token', None)
        return Response({'token': token_key})


obtain_auth_token = CustomObtainAuthToken.as_view()

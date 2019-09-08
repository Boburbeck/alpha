from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import renderers, status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from main.serializers import AuthTokenSerializer
from main.serializers import UserModelSerializer
from main.serializers import UserRegisterSerializer
from main.serializers import UserSelectSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import User


class UserAuthView(ObtainAuthToken):
    """
    post:
    return Token
    ###fields
    + username - **Email**
    + password - **String**
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.AdminRenderer)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSelectSerializer(instance=user)
        details = user_serializer.data
        details.update(token=token.key)
        return Response(details)


class LogOutView(viewsets.ViewSet):
    """
        GET:
        Logs out user
    """

    @action(methods=["GET"], detail=False, url_name='logout', url_path='logout')
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.all()


class UserViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
        ### Readme
        update:
        Method PUR
        Expected body
           {    'id': 1,
                'username': "TEST USER"
                'first_name': "TEST USER"
                'last_name': "TEST USER"
           }

    ###Fields
    + username - **Required** - **CharField**
    + first_name - **Not Required** - **CharField**
    + last_name - **Not Required** - **CharField**
    """

    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    model = User

    @action(methods=["GET"], detail=False, )
    def info(self, request):
        serializer = UserModelSerializer(self.request.user, many=False)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False)
    def register(self, request):
        serializer = UserRegisterSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def logout(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

from rest_framework import status, viewsets, mixins

from main.serializers import UserModelSerializer
from main.serializers import UserRegisterSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import User


class OrderStatsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, ):
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

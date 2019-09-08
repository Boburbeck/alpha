from rest_framework import status, viewsets, mixins

from main.serializers import NetCostModelSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from main.models import NetCost


class NetCostModelViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    """
        ### Readme
        list:
        Method GET
        Expected body
           {    'id': 1,
                'price': "5000"
                'product': {
                    "id": 1,
                    "name": "Product Name"
                }
                'creator': {
                    "id": 1,
                    "first_name": "First Name",
                    "last_name": "Lase Name"
                }
                'created_date': '2019-01-01 00-00-00.00000'
           }
        create:
        Method POST
        Expected body
           {
                'price': "5000"
                'product': 1
           }
    ###Fields
    + price - **Required** - **Decimal**
    + product - **Required** - **PK**
    """

    serializer_class = NetCostModelSerializer
    queryset = NetCost.objects.all()
    model = NetCost

from rest_framework import status, viewsets, mixins

from main.serializers import SoldCostModelSerializer
from main.models import SoldCost


class SoldCostModelViewSet(viewsets.GenericViewSet,
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

    serializer_class = SoldCostModelSerializer
    queryset = SoldCost.objects.all()
    model = SoldCost

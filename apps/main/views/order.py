from rest_framework import viewsets

from main.serializers import OrderModelSerializer
from main.models import Order


class OrderModelViewSet(viewsets.ModelViewSet):
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

    serializer_class = OrderModelSerializer
    queryset = Order.objects.all()
    model = Order

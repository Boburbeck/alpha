from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.serializers import OrderModelSerializer
from main.serializers import OrderChangeStatusSerializer
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

    @action(methods=['PUT'], detail=True)
    def order_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderChangeStatusSerializer(instance=order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Order
from stats.serializers import OrderStatsSerializer
from stats.serializers import OrderSubquery


class OrderStatsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, ):
    """
    TEST
    """

    serializer_class = OrderStatsSerializer
    queryset = Order.objects.all()
    model = Order

    @action(methods=["GET"], detail=False, )
    def sub_by_order(self, request):
        order = Order.objects.by_order()

        serializer = OrderSubquery(order, many=True)
        return Response(serializer.data)

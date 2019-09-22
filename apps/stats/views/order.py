from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Order
from stats.serializers import OrderStatsSerializer
from stats.serializers import OrderSubquery
from stats.serializers import OrderSubqueryCashier
from stats.serializers import ValidateCashier


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

    @action(methods=["GET"], detail=False, )
    def sub_by_cashier(self, request):
        cashier = ValidateCashier(data=request.GET)
        cashier.is_valid(raise_exception=True)
        cashier = cashier.validated_data.get('cashier')
        order = Order.objects.by_cashier(cashier)
        order = order.order_by('-sales')

        serializer = OrderSubqueryCashier(order, many=True)
        return Response(serializer.data)

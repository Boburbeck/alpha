from rest_framework import viewsets
from rest_framework.response import Response

from main.models import Stock
from stock.serializers import StockModelSerializer
from stock.serializers import StockListDetailSerializer
from stock.serializers import StockEmployeeSerializer
from rest_framework.decorators import action


class StockModelViewSet(viewsets.ModelViewSet):
    """
    TEST
    """

    # serializer_class = StockModelSerializer
    queryset = Stock.objects.all()
    model = Stock

    def get_serializer_class(self):
        if self.action == 'list':
            return StockListDetailSerializer
        if self.action == 'retrieve':
            return StockListDetailSerializer
        return StockModelSerializer

    @action(methods=["POST"], detail=True)
    def add_employees(self, request, pk=None):
        stock = self.get_object()
        serializer = StockEmployeeSerializer(instance=stock, data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

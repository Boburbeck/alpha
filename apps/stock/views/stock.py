from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Stock
from stock.serializers import StockModelSerializer
from stock.serializers import StockStaffSerializer


class StockModelViewSet(viewsets.ModelViewSet):
    """
    TEST
    """

    serializer_class = StockModelSerializer
    queryset = Stock.objects.all()
    model = Stock

    @action(methods=["GET"], detail=False)
    def employee_count(self, request):
        stock = Stock.objects.employees()
        serializer = StockStaffSerializer(stock, many=True)
        return Response(serializer.data)

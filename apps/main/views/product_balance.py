from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.serializers import ProductBalanceModelSerializer
from main.serializers import ProductListDetailSerializer
from main.models import ProductBalance


class ProductBalanceModelViewSet(viewsets.ModelViewSet):
    """
        TEST
    """

    serializer_class = ProductBalanceModelSerializer
    model = ProductBalance
    filter_fields = ("stock", "product")

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListDetailSerializer
        if self.action == 'retrieve':
            return ProductListDetailSerializer
        return ProductBalanceModelSerializer

    def get_queryset(self):
        queryset = ProductBalance.objects.products()
        return queryset

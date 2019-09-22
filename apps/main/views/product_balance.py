from rest_framework import viewsets

from main.serializers import ProductBalanceModelSerializer
from main.models import ProductBalance


class ProductBalanceModelViewSet(viewsets.ModelViewSet):
    """
        TEST
    """

    serializer_class = ProductBalanceModelSerializer
    queryset = ProductBalance.objects.all()
    model = ProductBalance

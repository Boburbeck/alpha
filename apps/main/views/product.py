from rest_framework import viewsets

from main.serializers import ProductModelSerializer
from main.models import Product


class ProductModelViewSet(viewsets.ModelViewSet):
    """
        TEST
    """

    serializer_class = ProductModelSerializer
    queryset = Product.objects.all()
    model = Product

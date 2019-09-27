from rest_framework import viewsets

from main.serializers import CategoryModelSerializer
from main.models import Category


class CategoryModelViewSet(viewsets.ModelViewSet):
    """
        TEST
    """

    serializer_class = CategoryModelSerializer
    queryset = Category.objects.all()
    model = Category
    filter_fields = ("is_parent", "parent")

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Transaction
from finance.serializers import TransactionModelSerializer
from finance.serializers import TransactionListDetailSerializer


class TransactionModelViewSet(viewsets.ModelViewSet):
    """
    TEST
    """

    queryset = Transaction.objects.all()
    model = Transaction

    def get_serializer_class(self):
        if self.action == 'list':
            return TransactionListDetailSerializer
        if self.action == 'retrieve':
            return TransactionListDetailSerializer
        return TransactionModelSerializer

    def get_queryset(self):
        return Transaction.objects.orders()

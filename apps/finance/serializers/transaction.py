from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.serializers import ClientSelectSerializer
from main.serializers import UserSelectSerializer
from stock.serializers import StockSelectSerializer
from main.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'income_amount',
            'spent_amount',
        )


class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'income_amount',
            'spent_amount',
            'transaction_type',
            'client',
            'order',
            'stock',
            'comment',
            'created_by',
        )
        read_only_fields = ("created_by",)

    def __init__(self, *args, **kwargs):
        super(TransactionModelSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def create(self, validated_data):
        income_amount = validated_data.get('income_amount', 0)
        spent_amount = validated_data.get('spent_amount', 0)
        transaction_type = validated_data.get('transaction_type')
        client = validated_data.get('client', None)
        order = validated_data.get('order', None)
        stock = validated_data.get('stock')
        comment = validated_data.get('comment', None)
        transaction = Transaction.objects.create(
            income_amount=income_amount,
            spent_amount=spent_amount,
            transaction_type=transaction_type,
            client=client,
            order=order,
            stock=stock,
            comment=comment,
            created_by=self.user,
        )
        return transaction

    def to_representation(self, instance):
        self.fields['client'] = ClientSelectSerializer()
        self.fields['stock'] = StockSelectSerializer()
        self.fields['created_by'] = UserSelectSerializer()
        return super(TransactionModelSerializer, self).to_representation(instance)


class TransactionListDetailSerializer(serializers.Serializer):
    order = serializers.IntegerField()
    stock = serializers.IntegerField()
    available = serializers.DecimalField(max_digits=20, decimal_places=9)

    def to_representation(self, instance):
        self.fields['order'] = serializers.CharField(source="order_id")
        self.fields['stock'] = serializers.CharField(source="stock_id")
        return super(TransactionListDetailSerializer, self).to_representation(instance)

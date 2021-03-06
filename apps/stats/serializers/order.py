from rest_framework import serializers
from django.db.models import F
# Project
from main.models import Order

from main.serializers import ClientSelectSerializer
from main.serializers import UserSelectSerializer


class OrderStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'cashier',
            'payment_type',
            'status',
            'client',
            'total_price',
            'total_balance',
            'deliver',
            'delivery_man',
            'delivery_date',
            'delivery_price',
            'delivered',
            'created_date',
            'products',
        )

    def to_representation(self, instance):
        self.fields['cashier'] = UserSelectSerializer()
        self.fields['client'] = ClientSelectSerializer()
        return super(OrderStatsSerializer, self).to_representation(instance)


class OrderSubquery(serializers.Serializer):
    id = serializers.IntegerField()
    children_total = serializers.DecimalField(max_digits=20, decimal_places=9)
    internal_total_price = serializers.DecimalField(max_digits=20, decimal_places=9)
    internal_total_balance = serializers.DecimalField(max_digits=20, decimal_places=9)
    internal_delivery_price = serializers.DecimalField(max_digits=20, decimal_places=9)


class OrderSubqueryCashier(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    sales = serializers.DecimalField(max_digits=20, decimal_places=9)


class ValidateCashier(serializers.Serializer):
    from main.models import User
    cashier = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


class StockSubquerySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    total = serializers.DecimalField(max_digits=20, decimal_places=9)

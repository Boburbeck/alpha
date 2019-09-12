from rest_framework import serializers
from django.db.models import F
# Project
from main.models import Order

from main.serializers import ClientSelectSerializer
from main.serializers import UserSelectSerializer


class OrderStatsSerializer(serializers.ModelSerializer):
    f_exp = serializers.SerializerMethodField()

    def get_f_Exp(self, obj):
        result = F(obj.total_balace) + 100
        return result

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
            'f_exp'
        )

    def to_representation(self, instance):
        self.fields['cashier'] = UserSelectSerializer()
        self.fields['client'] = ClientSelectSerializer()
        return super(OrderStatsSerializer, self).to_representation(instance)

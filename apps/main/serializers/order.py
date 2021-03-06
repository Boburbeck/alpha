from decimal import Decimal

from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Order
from main.helpers import init_order_product
from main.helpers import init_order

from main.serializers import OrderProductModelSerializer
from main.serializers import ClientSelectSerializer
from main.serializers import UserSelectSerializer


class OrderSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'status')


class OrderModelSerializer(serializers.ModelSerializer):
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
            'products'
        )

    def __init__(self, *args, **kwargs):
        super(OrderModelSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            self.user = self.context['request'].user

        self.view = self.context['view']
        if self.view.action != 'list':
            self.fields['products'] = OrderProductModelSerializer(many=True, required=True)

    @transaction.atomic
    def create(self, data):
        order_number = data.get('order_number')
        cashier = data.get('cashier')
        payment_type = data.get('payment_type')
        client = data.get('client')
        deliver = data.get('deliver', False)
        delivery_man = data.get('delivery_man', None)
        delivery_date = data.get('delivery_date', None)
        delivery_price = data.get('delivery_price', None)
        products = data.get('products')
        order = Order.objects.create(
            order_number=order_number,
            cashier=cashier,
            payment_type=payment_type,
            client=client,
            deliver=deliver,
            delivery_man=delivery_man,
            delivery_date=delivery_date,
            delivery_price=delivery_price,
            total_price=0,
            created_by=self.user,
        )
        for product in products:
            init_order_product(product, order)
        init_order(order)
        return order

    def to_representation(self, instance):
        self.fields['cashier'] = UserSelectSerializer()
        self.fields['client'] = ClientSelectSerializer()
        return super(OrderModelSerializer, self).to_representation(instance)


class OrderChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'status',
            'modified_date',
        )
        read_only_fields = ("order_number",)

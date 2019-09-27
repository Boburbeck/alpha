from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Order, OrderProduct
from main.helpers import order_product_price
from main.helpers import product_availability
from main.helpers import init_create_product_balance


class OrderProductSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'price')


class OrderProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = (
            'id',
            'order',
            'product',
            'stock',
            'amount',
            'price',
            'created_date'
        )
        read_only_fields = ('order', 'price')

    def validate(self, attrs):
        self._errors = dict()
        product = attrs.get('product')
        stock = attrs.get('stock')

        if not product:
            self._errors.update({'product': _('This field is required')})

        if not attrs.get('amount') and not attrs.get('amount') > 0:
            self._errors.update({'price': _('This field should not be less than 1 or be empty')})

        available = product_availability(product, stock)
        if available.get('available', 0) < attrs.get("amount"):
            self._errors.update({'product_balance': _('There is not enough product in the stock')})

        if self._errors:
            raise serializers.ValidationError(self._errors)

        return attrs

    @transaction.atomic
    def create(self, data):
        product = data.get('product'),
        stock = data.get('stock'),
        amount = data.get('amount'),
        price = order_product_price(product, amount)
        order_product = OrderProduct.objects.create(
            order=data.get('order'),
            product=product,
            stock=stock,
            amount=amount,
            price=price,
            internal_price=price,
        )
        init_create_product_balance(stock=stock, product=product, amount=amount)
        return order_product

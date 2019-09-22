from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Order, OrderProduct
from main.helpers import order_product_price


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
            'amount',
            'price',
            'created_date'
        )
        read_only_fields = ('order', 'price')

    def validate(self, attrs):
        self._errors = dict()

        if not attrs.get('product'):
            self._errors.update({'product': _('This field is required')})

        if not attrs.get('amount') and not attrs.get('amount') > 0:
            self._errors.update({'price': _('This field should not be less than 1 or be empty')})

        if self._errors:
            raise serializers.ValidationError(self._errors)

        return attrs

    @transaction.atomic
    def create(self, data):
        product = data.get('product'),
        amount = data.get('amount'),
        price = order_product_price(product, amount)
        order_product = OrderProduct.objects.create(
            order=data.get('order'),
            product=product,
            amount=amount,
            price=price,
            internal_price=price,
        )
        return order_product
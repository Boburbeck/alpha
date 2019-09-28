from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
# Project
from main.models import SoldCost, Product
from main.serializers import UserSelectSerializer
from main.serializers import ProductSelectSerializer
from main.helpers import mark_sold_cost_false


class SoldCostSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldCost
        fields = ('id', 'product', 'price')


class SoldCostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldCost
        fields = (
            'id',
            'product',
            'price',
            'is_active',
            'creator',
            'created_date',
        )

    def __init__(self, *args, **kwargs):
        super(SoldCostModelSerializer, self).__init__(*args, **kwargs)
        if self.context.get('request'):
            self.user = self.context['request'].user

    def validate(self, attrs):
        self._errors = dict()
        if not attrs.get('product'):
            self._errors.update({'product': _('This field is required')})

        if not attrs.get('price'):
            self._errors.update({'price': _('This field is required')})

        if self._errors:
            raise serializers.ValidationError(self._errors)

        return attrs

    @transaction.atomic
    def create(self, data):
        mark_sold_cost_false(data.get('product'))
        price = data.get('price')
        product: Product = data.get('product')
        creator = self.user
        net_cost = SoldCost.objects.create(
            price=price,
            product=product,
            creator=creator
        )
        return net_cost

    def to_representation(self, instance):
        self.fields['creator'] = UserSelectSerializer()
        self.fields['product'] = ProductSelectSerializer()
        return super(SoldCostModelSerializer, self).to_representation(instance)

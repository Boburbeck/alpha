from django.db import transaction
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
# Project
from main.models import NetCost, Product
from main.serializers import UserSelectSerializer
from main.serializers import ProductSelectSerializer
from main.helpers import mark_net_cost_false


class NetCostSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetCost
        fields = ('id', 'product', 'price')


class NetCostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetCost
        fields = (
            'id',
            'product',
            'price',
            'is_active',
            'creator',
            'created_date'
        )

    def __init__(self, *args, **kwargs):
        super(NetCostModelSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

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
        mark_net_cost_false(data.get('product'))
        price = data.get('price')
        product: Product = data.get('product')
        creator = self.user
        net_cost = NetCost.objects.create(
            price=price,
            product=product,
            creator=creator
        )
        return net_cost

    def to_representation(self, instance):
        self.fields['creator'] = UserSelectSerializer()
        self.fields['product'] = ProductSelectSerializer()
        return super(NetCostModelSerializer, self).to_representation(instance)

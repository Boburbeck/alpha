from rest_framework import serializers

# Project
from main.models import ProductBalance
from main.serializers import ProductSelectSerializer
from stock.serializers import StockSelectSerializer


class ProductBalanceSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBalance
        fields = (
            'id',
            'balance',
            'product',
            'stock',
        )


class ProductBalanceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBalance
        fields = (
            'id',
            'balance',
            'defect',
            'product',
            'stock',
            'created_date'
        )

    def to_representation(self, instance):
        self.fields['product'] = ProductSelectSerializer()
        self.fields['stock'] = StockSelectSerializer()
        return super(ProductBalanceModelSerializer, self).to_representation(instance)

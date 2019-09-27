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
            'sold',
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
            'sold',
            'product',
            'stock',
            'created_date'
        )

    def to_representation(self, instance):
        self.fields['product'] = ProductSelectSerializer()
        self.fields['stock'] = StockSelectSerializer()
        return super(ProductBalanceModelSerializer, self).to_representation(instance)


class ProductListDetailSerializer(serializers.Serializer):
    total_balance = serializers.DecimalField(max_digits=20, decimal_places=9)
    total_defect = serializers.DecimalField(max_digits=20, decimal_places=9)
    total_sold = serializers.DecimalField(max_digits=20, decimal_places=9)
    available = serializers.DecimalField(max_digits=20, decimal_places=9)

    def to_representation(self, instance):
        self.fields['product'] = serializers.CharField(source="product_id")
        self.fields['stock'] = serializers.CharField(source="stock_id")
        return super(ProductListDetailSerializer, self).to_representation(instance)

from rest_framework import serializers

# Project
from main.models import Product


class ProductSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')

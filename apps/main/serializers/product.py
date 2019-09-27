from rest_framework import serializers

# Project
from main.models import Product
from main.serializers import UserSelectSerializer
from main.serializers import CategorySelectSerializer


class ProductSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'name',
            'ball',
            'code',
            'comment',
            'priority',
            'creator',
            'created_date'
        )
        read_only_fields = ("creator",)

    def to_representation(self, instance):
        self.fields['category'] = CategorySelectSerializer()
        self.fields['creator'] = UserSelectSerializer()
        return super(ProductModelSerializer, self).to_representation(instance)

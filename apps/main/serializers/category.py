from rest_framework import serializers

# Project
from main.models import Category


class CategorySelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'is_parent',
            'parent',
            'created_date'
        )
        read_only_fields = ("creator",)

    def to_representation(self, instance):
        self.fields['parent'] = CategorySelectSerializer()
        return super(CategoryModelSerializer, self).to_representation(instance)

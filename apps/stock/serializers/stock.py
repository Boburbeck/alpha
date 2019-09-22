from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Stock

from main.serializers import UserSelectSerializer


class StockSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
        )


class StockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'address',
            'employees',
            'created_by',
            'created_date',
        )
        read_only_fields = ("created_by",)

    def __init__(self, *args, **kwargs):
        super(StockModelSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def validate(self, attrs):
        self._errors = dict()

        # if not attrs.get('product'):
        #     self._errors.update({'product': _('This field is required')})

        if self._errors:
            raise serializers.ValidationError(self._errors)
        return attrs

    def create(self, validated_data):
        employees = validated_data.get('employees', [])
        stock = Stock.objects.create(
            name=validated_data.get('name'),
            address=validated_data.get('address', None),
            created_by=self.user
        )
        if employees:
            for employee in employees:
                stock.employees.add(employee)
        return stock

    def to_representation(self, instance):
        self.fields['created_by'] = UserSelectSerializer()
        return super(StockModelSerializer, self).to_representation(instance)


class StockListDetailSerializer(serializers.ModelSerializer):
    employees = UserSelectSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'address',
            'employees',
            'created_by',
            'created_date',
        )
        read_only_fields = ("created_by",)

    def to_representation(self, instance):
        self.fields['created_by'] = UserSelectSerializer()
        return super(StockListDetailSerializer, self).to_representation(instance)


# class StockEmployeeSerializer(serializers.ListSerializer):
#     employees = serializers.ListField(child=serializers.IntegerField(min_value=1))
#
#     def update(self, instance: Stock, validated_data):
#         employees = validated_data['employees']
#         instance.employees = employees
#         instance.save()
#         return instance

class StockEmployeeSerializer(serializers.ModelSerializer):
    # employees = UserSelectSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'address',
            'employees',
            'created_by',
            'created_date',
        )
        read_only_fields = ("created_by", 'name', 'address')

    def update(self, instance: Stock, validated_data):
        employees = validated_data.get('employees', [])
        for employee in employees:
            instance.employees.add(employee)
        return instance

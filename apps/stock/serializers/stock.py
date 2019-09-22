from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Stock
from main.helpers import init_set_permission
from main.helpers import init_create_membership


class StockSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
        )


class StockModelSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField()

    def get_employees(self, obj):
        from stock.serializers import MembershipStockSerializer
        if obj.get_members:
            return MembershipStockSerializer(obj.get_members(), many=True).data

    class Meta:
        model = Stock
        fields = (
            'id',
            'name',
            'address',
            'employees',
            'created_date',
        )

    def __init__(self, *args, **kwargs):
        super(StockModelSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def create(self, validated_data):
        from main.models.stock import Membership
        stock = Stock.objects.create(
            name=validated_data.get('name'),
            address=validated_data.get('address', None),
        )
        init_create_membership(stock, self.user, Membership.OWNER)
        return stock


class StockStaffSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    staff = serializers.DecimalField(max_digits=20, decimal_places=9)

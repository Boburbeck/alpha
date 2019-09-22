from rest_framework import serializers
from django.utils.translation import gettext as _
# Project
from main.models import Membership
from main.serializers import UserSelectSerializer


class MembershipSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            'id',
            'stock',
            'member',
            'role',
        )


class MembershipStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            'member',
            'role',
        )

    def to_representation(self, instance):
        self.fields['member'] = UserSelectSerializer()
        return super(MembershipStockSerializer, self).to_representation(instance)


class MembershipModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = (
            'id',
            'stock',
            'member',
            'date_joined',
            'role',
            'created_date',
        )

    def __init__(self, *args, **kwargs):
        super(MembershipModelSerializer, self).__init__(*args, **kwargs)
        self.user = self.context.get('request').user

    def create(self, validated_data):
        membership = Membership.objects.create(
            stock=validated_data.get('stock'),
            member=validated_data.get('member'),
            date_joined=validated_data.get('date_joined'),
            role=validated_data.get('role'),
        )
        return membership

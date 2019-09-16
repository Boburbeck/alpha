from rest_framework import serializers

# Project
from main.models import Client


class ClientSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name')

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

# Project
from main.models import User


class UserSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_('Username'))
    password = serializers.CharField(label=_('Password'), style={'input_type': 'password'})

    def validate(self, attrs):
        self._errors = {}
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:

            if self._errors:
                raise serializers.ValidationError(self._errors)

            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers. \
                        ValidationError([msg], code='authorization')

            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError([msg], code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError([msg], code='authorization')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_active',
            'staff',
            'is_admin',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance: User, validated_data):
        username = validated_data.get('username', None)
        first_name = validated_data.get('first_name')
        last_name = validated_data.pop('last_name', None)

        instance.username = username
        instance.first_name = first_name
        instance.last_name = last_name

        instance.save()
        return instance


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)
    password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        user_obj = User.objects.create(
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
        )
        user_obj.set_password(validated_data.get('password'))
        user_obj.save()
        return user_obj

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from common.serializers.mixins import ExtendedModelSerializer
from staff.models import Manager
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class ManagerSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'level', 'manage_role')


class ManagerSearchSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'level', 'manage_role')


class ManagerCreateSerializer(ExtendedModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Manager
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'level',
            'manage_role',

        )

        def create(self, validated_data):
            user_data = {
                'first_name': validated_data.pop('first_name'),
                'last_name': validated_data.pop('last_name'),
                'email': validated_data.pop('email'),
                'password': validated_data.pop('password'),

            }

            with transaction.atomic():
                user = User.objects.create_user(**user_data)
                validated_data['user'] = user

                instance = super().create(validated_data)
            return instance


class ManagerListSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Manager
        fields = ('user', 'level', 'manage_role')


class ManagerUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Manager
        fields = ('level', 'manage_role')

    def update(self, instance, validated_data):
        category_data = validated_data.pop('level', instance.category)
        role_data = validated_data.pop('manage_role', instance.role)

        instance = super().update(instance, validated_data)
        instance.category.set(*[category_data])
        instance.role.set(*[role_data])

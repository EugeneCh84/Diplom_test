from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from common.serializers.mixins import ExtendedModelSerializer
from staff.models import Employee
from users.serializers.nested.users import UserShortSerializer

User = get_user_model()


class EmployeeSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'category', 'role')


class EmployeeSearchSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'category', 'role')


class EmployeeCreateSerializer(ExtendedModelSerializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'password',

        )

        def create(self, validated_data):
            user_data = {
                'first_name': validated_data.pop('first_name'),
                'last_name': validated_data.pop('last_name'),
                'email': validated_data.pop('email'),
                'password': validated_data.pop('password'),

            }

            with transaction.atomic():
                user = User.objects.create(**user_data)
                validated_data['user'] = user

                instance = super().create(validated_data)
            return instance


class EmployeeListSerializer(ExtendedModelSerializer):
    user = UserShortSerializer()

    class Meta:
        model = Employee
        fields = ('user', 'category', 'role')


class EmployeeUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Employee
        fields = ('category', 'role')

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category', instance.category)
        role_data = validated_data.pop('role', instance.role)

        instance = super().update(instance, validated_data)
        instance.category.set(*[category_data])
        instance.role.set(*[role_data])

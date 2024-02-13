from django.db import transaction

from common.serializers.mixins import ExtendedModelSerializer
from clients.models import Client
from rest_framework import serializers


class ClientSerializer(ExtendedModelSerializer):
    class Meta:
        model = Client
        fields = ('company_name', 'phone', 'email', 'address', 'zipcode', 'status', 'discount')


class ClientSearchSerializer(ExtendedModelSerializer):
    class Meta:
        model = Client
        fields = ('company_name', 'status', 'email')


class ClientCreateSerializer(ExtendedModelSerializer):
    company_name = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    address = serializers.CharField(write_only=True)
    zipcode = serializers.IntegerField(write_only=True)
    status = serializers.CharField(write_only=True)
    discount = serializers.IntegerField(write_only=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'company_name',
            'phone',
            'email',
            'address',
            'zipcode',
            'status',
            'discount',

        )

        def create(self, validated_data):

            return Client.object.create(**validated_data)


class ClientListSerializer(ExtendedModelSerializer):
    class Meta:
        model = Client
        fields = ('company_name',
                  'phone',
                  'email',
                  'address',
                  'zipcode',
                  'status',
                  'discount',
                  )


class ClientUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Client
        fields = ('status', 'discount')

    def update(self, instance, validated_data):
        status_data = validated_data.pop('status', instance.description)
        discount_data = validated_data.pop('discount', instance.price)

        instance = super().update(instance, validated_data)
        instance.status.set(*[status_data])
        instance.discount.set(*[discount_data])

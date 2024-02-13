from django.db import transaction

from common.serializers.mixins import ExtendedModelSerializer
from equipment.models import Equipment
from rest_framework import serializers


class EquipmentSerializer(ExtendedModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', 'manufacturer', 'description', 'type', 'price', 'image')


class EquipmentSearchSerializer(ExtendedModelSerializer):
    class Meta:
        model = Equipment
        fields = ('name', 'manufacturer', 'type')


class EquipmentCreateSerializer(ExtendedModelSerializer):

    class Meta:
        model = Equipment
        fields = (
            'id',
            'name',
            'manufacturer',
            'description',
            'type',
            'price',
            'image',

        )

        def create(self, validated_data):

            return Equipment.object.create(**validated_data)


class EquipmentListSerializer(ExtendedModelSerializer):
    class Meta:
        model = Equipment
        fields = ('name', 'manufacturer', 'description', 'type', 'price', 'image')


class EquipmentUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = Equipment
        fields = ('description', 'price')

    def update(self, instance, validated_data):
        description_data = validated_data.pop('description', instance.description)
        price_data = validated_data.pop('price', instance.price)

        instance = super().update(instance, validated_data)
        instance.description.set(*[description_data])
        instance.price.set(*[price_data])

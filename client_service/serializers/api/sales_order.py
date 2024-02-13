from django.db import transaction

from common.serializers.mixins import ExtendedModelSerializer
from client_service.models import ServiceOrder, SalesOrder
from clients.serializers.api.clients import ClientSerializer
from equipment.models import Equipment
from equipment.serializers.api.equipment import EquipmentSerializer
from staff.serializers.api.manager import ManagerSerializer
from clients.models import Client
from staff.models import Manager


class SalesSearchSerializer(ExtendedModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ('order_code', 'customer', 'order_date')


class SalesCreateSerializer(ExtendedModelSerializer):
    customer = ClientSerializer(read_only=True)
    manager = ManagerSerializer(read_only=True)
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = (
            'order_code',
            'customer',
            'manager',
            'equipment',
            'quantity',
            'price',

        )

        def create(self, validated_data):
            customer_data = validated_data.pop("customer")
            manager_data = validated_data.pop("manager")
            equipment_data = validated_data.pop("equipment")
            customer_obj = Client.objects.create(company_name=customer_data['company_name'],
                                                 status=customer_data['status'],
                                                 discount=customer_data['discount'],
                                                 )

            manager_obj = Manager.objects.create(name=manager_data['name'],
                                                 level=manager_data['level'],
                                                 manage_role=manager_data['manage_role'],
                                                 )

            equipment_obj = Equipment.objects.create(name=equipment_data['name'],
                                                     manufacturer=equipment_data['manufacturer'],
                                                     price=equipment_data['price'],
                                                     )
            self.instance = SalesOrder.objects.create(order_code=validated_data('order_code'),
                                                      customer=customer_obj,
                                                      manager=manager_obj,
                                                      equipment=equipment_obj,
                                                      quantity=validated_data['quantity'],
                                                      price=validated_data['price'],
                                                      )
            return validated_data


class SalesListSerializer(ExtendedModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ('__all__')


class SalesUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ('quantity', 'price')

    def update(self, instance, validated_data):
        quantity_data = validated_data.pop('quantity', instance.quantity)
        price_data = validated_data.pop('price', instance.price)

        instance = super().update(instance, validated_data)
        instance.description.set(*[quantity_data])
        instance.price.set(*[price_data])

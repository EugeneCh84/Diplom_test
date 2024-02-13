from django.db import transaction

from common.serializers.mixins import ExtendedModelSerializer
from client_service.models import ServiceOrder, SalesOrder
from clients.serializers.api.clients import ClientSerializer
from equipment.models import Equipment
from staff.serializers.api.employee import EmployeeSerializer
from staff.serializers.api.manager import ManagerSerializer
from clients.models import Client
from staff.models import Manager


class ServiceSearchSerializer(ExtendedModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ('order_code', 'customer', 'order_date')


class ServiceCreateSerializer(ExtendedModelSerializer):
    customer = ClientSerializer(read_only=True)
    manager = ManagerSerializer(read_only=True)
    engineer = EmployeeSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceOrder
        fields = (
            'order_code',
            'customer',
            'manager',
            'engineer',
            'type',
            'difficulty',

        )

        def create(self, validated_data):
            customer_data = validated_data.pop("customer")
            manager_data = validated_data.pop("manager")
            engineer_data = validated_data.pop("engineer")
            customer_obj = Client.objects.create(company_name=customer_data['company_name'],
                                                 status=customer_data['status'],
                                                 discount=customer_data['discount'],
                                                 )

            manager_obj = Manager.objects.create(name=manager_data['name'],
                                                 level=manager_data['level'],
                                                 manage_role=manager_data['manage_role'],
                                                 )

            engineer_obj = Equipment.objects.create(name=engineer_data['name'],
                                                    category=engineer_data['category'],
                                                    role=engineer_data['role'],
                                                    )
            self.instance = SalesOrder.objects.create(order_code=validated_data('order_code'),
                                                      customer=customer_obj,
                                                      manager=manager_obj,
                                                      engineer=engineer_obj,
                                                      type=validated_data['type'],
                                                      difficulty=validated_data['difficulty'],
                                                      )
            return validated_data


class ServiceListSerializer(ExtendedModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ('__all__')


class ServiceUpdateSerializer(ExtendedModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ('type', 'difficulty')

    def update(self, instance, validated_data):
        description_data = validated_data.pop('type', instance.description)
        price_data = validated_data.pop('difficulty', instance.price)

        instance = super().update(instance, validated_data)
        instance.description.set(*[description_data])
        instance.price.set(*[price_data])

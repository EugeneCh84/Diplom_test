from django.db import models
from common.models.mixins import InfoMixin
from clients.models import Client
from equipment.models import Equipment
from staff.models import Manager, Employee
from users.models.users import User


class SalesOrder(InfoMixin):
    order_code = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    customer = models.ForeignKey(Client, related_name='sales_order', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, related_name='sales_order', on_delete=models.PROTECT)
    equipment = models.ForeignKey(Equipment, related_name='sales_order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    price = models.PositiveIntegerField(blank=True, null=True, default=0)
    # created_by = models.ForeignKey(User, related_name='sales_order', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)

    # modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_code} / {self.customer}'


class ServiceOrder(InfoMixin):
    MAINTENANCE = 'maintenance'
    COMMISSIONING = 'commissioning'
    CHOICES_TYPE = (
        (MAINTENANCE, 'Maintenance'),
        (COMMISSIONING, 'Commissioning'),
    )

    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    CHOICES_DIFFICULTY = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
    )

    order_code = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    customer = models.ForeignKey(Client, related_name='service_order', on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, related_name='service_order', on_delete=models.PROTECT)
    engineer = models.ForeignKey(Employee, related_name='service_order', on_delete=models.PROTECT)
    equipment = models.ForeignKey(Equipment, related_name='service_order', on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=CHOICES_TYPE, blank=False, null=False)
    difficulty = models.CharField(max_length=20, choices=CHOICES_DIFFICULTY, blank=False, null=False)
    # created_by = models.ForeignKey(User, related_name='service_order', on_delete=models.PROTECT)
    order_date = models.DateTimeField(auto_now_add=True)

    # modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.order_code} / {self.customer}'

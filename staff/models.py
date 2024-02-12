from django.db import models

from users.models.users import User


class Manager(models.Model):
    LOW = 'low'
    HIGH = 'high'
    CHOICES_LEVEL = (
        (LOW, 'Low'),
        (HIGH, 'High'),
    )

    SALES = 'sales'
    WARRANTY = 'warranty'
    CHOICES_TYPE = (
        (SALES, 'Sales'),
        (WARRANTY, 'Warranty'),
    )

    name = models.OneToOneField(User, related_name='manager', on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=CHOICES_LEVEL, default=LOW)
    manage_role = models.CharField(max_length=20, choices=CHOICES_TYPE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}  ---  {self.manage_role}'


class Employee(models.Model):
    FIRST_CATEGORY = 'first_category'
    SECOND_CATEGORY = 'second_category'
    THIRD_CATEGORY = 'third_category'
    LEAD_ENGINEER = 'lead_engineer'

    CHOICES_CATEGORY = (
        (FIRST_CATEGORY, 'First Category'),
        (SECOND_CATEGORY, 'Second Category'),
        (THIRD_CATEGORY, 'Third Category'),
        (LEAD_ENGINEER, 'Lead Engineer'),
    )

    ELECTRONICS = 'electronics'
    MECHANICS = 'mechanics'
    UNIVERSAL = 'universal'

    CHOICES_ROLE = (
        (ELECTRONICS, 'Electronics'),
        (MECHANICS, 'Mechanics'),
        (UNIVERSAL, 'Universal'),
    )

    name = models.OneToOneField(User, related_name='employee', on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CHOICES_CATEGORY, default=FIRST_CATEGORY)
    role = models.CharField(max_length=20, choices=CHOICES_ROLE, default=UNIVERSAL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} ---  {self.category}'



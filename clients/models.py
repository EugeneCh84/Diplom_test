from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from common.models.mixins import InfoMixin


class Client(InfoMixin):
    NEW = 'new'
    OLD = 'old'
    VIP = 'vip'
    CHOICES_STATUS = (
        (NEW, 'New'),
        (OLD, 'Old'),
        (VIP, 'VIP'),
    )

    company_name = models.CharField(max_length=255, blank=False, null=False)
    phone = PhoneNumberField(max_length=15, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    zipcode = models.PositiveSmallIntegerField(blank=False, null=False)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, blank=False, null=False)
    discount = models.PositiveSmallIntegerField(default=0, validators=([MaxValueValidator(50)]),
                                                blank=False, null=False)

    # created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.company_name}'

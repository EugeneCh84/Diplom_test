from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):

    phone_number = PhoneNumberField(verbose_name='Phone Number', unique=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

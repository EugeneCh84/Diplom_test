from django.db import models
from common.models.mixins import InfoMixin


class Equipment(InfoMixin):
    MACHINE = 'machine'
    TOOL = 'tool'
    OTHER = 'other'
    SPAREPART = 'sparepart'

    TYPE_CHOICES = (
        (MACHINE, 'Machine'),
        (TOOL, 'Tool'),
        (OTHER, 'Other'),
        (SPAREPART, 'Sparepart'),
    )
    name = models.CharField(max_length=100, blank=False, null=False)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=False, null=False)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'
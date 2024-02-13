from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from common.views.mixins import LCRUDViewSet
from equipment.models import Equipment
from equipment.serializers.api import equipment as equipments_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of equipment', tags=['Equipment']),
    create=extend_schema(summary='Create equipment', tags=['Equipment']),
    update=extend_schema(summary='Change equipment', tags=['Equipment']),
    partial_update=extend_schema(summary='Change equipment partialy', tags=['Equipment']),
    destroy=extend_schema(summary='Delete equipment', tags=['Equipment']),
    search=extend_schema(filters=True, summary='Search equipment', tags=['Dicts']),
)
class EquipmentView(LCRUDViewSet):
    queryset = Equipment.objects.all()
    serializer_class = equipments_s.EquipmentListSerializer

    multi_serializer_class = {
        'list': equipments_s.EquipmentListSerializer,
        'create': equipments_s.EquipmentCreateSerializer,
        'update': equipments_s.EquipmentUpdateSerializer,
        'partial_update': equipments_s.EquipmentUpdateSerializer,
        'search': equipments_s.EquipmentSearchSerializer,
        'destroy': equipments_s.EquipmentSearchSerializer,
    }

    lookup_url_kwarg = 'equipment_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        )

    def get_queryset(self):
        qs = Equipment.objects.select_related(
            'name',
            'manufacturer',
            'description',
            'type',
            'price',
            'image',

        )
        return qs

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=dict())
        serializer.is_valid(raise_exception=True)
        return super().destroy(request, *args, **kwargs)


from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter

from client_service.models import ServiceOrder
from common.views.mixins import LCRUDViewSet
from client_service.serializers.api import service_order as service_order_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of Service', tags=['Service']),
    create=extend_schema(summary='Create Service', tags=['Service']),
    update=extend_schema(summary='Change Service', tags=['Service']),
    partial_update=extend_schema(summary='Change Service partialy', tags=['Service']),
    destroy=extend_schema(summary='Delete Service', tags=['Service']),
    search=extend_schema(filters=True, summary='Search Sales', tags=['Dicts']),
)
class ServiceView(LCRUDViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = service_order_s.ServiceListSerializer

    multi_serializer_class = {
        'list': service_order_s.ServiceListSerializer,
        'create': service_order_s.ServiceCreateSerializer,
        'update': service_order_s.ServiceUpdateSerializer,
        'partial_update': service_order_s.ServiceUpdateSerializer,
        'search': service_order_s.ServiceSearchSerializer,
        'destroy': service_order_s.ServiceSearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )

    def get_queryset(self):
        qs = ServiceOrder.objects.select_related(
            'order_code',
            'customer',
            'manager',
            'equipment',
            'type',
            'difficulty',

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

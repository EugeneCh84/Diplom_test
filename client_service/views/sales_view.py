from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter

from client_service.models import SalesOrder
from common.views.mixins import LCRUDViewSet
from client_service.serializers.api import sales_order as sales_order_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of Sales', tags=['Sales']),
    create=extend_schema(summary='Create Sales', tags=['Sales']),
    update=extend_schema(summary='Change Sales', tags=['Sales']),
    partial_update=extend_schema(summary='Change Sales partialy', tags=['Sales']),
    destroy=extend_schema(summary='Delete Sales', tags=['Sales']),
    search=extend_schema(filters=True, summary='Search Sales', tags=['Dicts']),
)
class SalesView(LCRUDViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = sales_order_s.SalesListSerializer

    multi_serializer_class = {
        'list': sales_order_s.SalesListSerializer,
        'create': sales_order_s.SalesCreateSerializer,
        'update': sales_order_s.SalesUpdateSerializer,
        'partial_update': sales_order_s.SalesUpdateSerializer,
        'search': sales_order_s.SalesSearchSerializer,
        'destroy': sales_order_s.SalesSearchSerializer,
    }

    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )

    def get_queryset(self):
        qs = SalesOrder.objects.select_related(
            'order_code',
            'customer',
            'manager',
            'equipment',
            'quantity',
            'price',

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

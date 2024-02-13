from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from common.views.mixins import LCRUDViewSet
from clients.models import Client
from clients.serializers.api import clients as clients_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of clients', tags=['Clients']),
    create=extend_schema(summary='Create clients', tags=['Clients']),
    update=extend_schema(summary='Change clients', tags=['Clients']),
    partial_update=extend_schema(summary='Change clients partialy', tags=['Clients']),
    destroy=extend_schema(summary='Delete clients', tags=['Clients']),
    search=extend_schema(filters=True, summary='Search clients', tags=['Dicts']),
)
class ClientView(LCRUDViewSet):
    queryset = Client.objects.all()
    serializer_class = clients_s.ClientListSerializer

    multi_serializer_class = {
        'list': clients_s.ClientListSerializer,
        'create': clients_s.ClientCreateSerializer,
        'update': clients_s.ClientUpdateSerializer,
        'partial_update': clients_s.ClientUpdateSerializer,
        'search': clients_s.ClientSearchSerializer,
        'destroy': clients_s.ClientSearchSerializer,
    }

    lookup_url_kwarg = 'clients_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        )

    def get_queryset(self):
        qs = Client.objects.select_related(
            'id',
            'company_name',
            'phone',
            'email',
            'address',
            'zipcode',
            'status',
            'discount',

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



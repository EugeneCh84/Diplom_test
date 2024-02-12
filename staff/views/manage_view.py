from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from common.views.mixins import LCRUDViewSet
from staff.models import Manager
from staff.serializers.api import manager as managers_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of managers', tags=['Company:']),
    create=extend_schema(summary='Create managers', tags=['Company:']),
    update=extend_schema(summary='Change managers', tags=['Company:']),
    partial_update=extend_schema(summary='Change managers partialy', tags=['Company:']),
    destroy=extend_schema(summary='Delete managers', tags=['Company:']),
    search=extend_schema(filters=True, summary='Search managers', tags=['Dicts']),
)
class ManagerView(LCRUDViewSet):
    queryset = Manager.objects.all()
    serializer_class = managers_s.ManagerListSerializer

    multi_serializer_class = {
        'list': managers_s.ManagerListSerializer,
        'create': managers_s.ManagerCreateSerializer,
        'update': managers_s.ManagerUpdateSerializer,
        'partial_update': managers_s.ManagerUpdateSerializer,
        'search': managers_s.ManagerSearchSerializer,
        'destroy': managers_s.ManagerSearchSerializer,
    }

    lookup_url_kwarg = 'user_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        )

    def get_queryset(self):
        qs = Manager.objects.select_related(
            'user',
            'level',
            'manage_role',

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

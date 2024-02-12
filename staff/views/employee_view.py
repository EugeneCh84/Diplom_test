from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from common.views.mixins import LCRUDViewSet
from staff.models import Employee
from staff.serializers.api import employee as employees_s
from rest_framework.decorators import action


@extend_schema_view(
    list=extend_schema(summary='List of engineers', tags=['Company:']),
    create=extend_schema(summary='Create engineer', tags=['Company:']),
    update=extend_schema(summary='Change engineer', tags=['Company:']),
    partial_update=extend_schema(summary='Change engineer partialy', tags=['Company:']),
    destroy=extend_schema(summary='Delete engineer', tags=['Company:']),
    search=extend_schema(filters=True, summary='Search engineer', tags=['Dicts']),
)
class EmployeeView(LCRUDViewSet):
    queryset = Employee.objects.all()
    serializer_class = employees_s.EmployeeListSerializer

    multi_serializer_class = {
        'list': employees_s.EmployeeListSerializer,
        'create': employees_s.EmployeeCreateSerializer,
        'update': employees_s.EmployeeUpdateSerializer,
        'partial_update': employees_s.EmployeeUpdateSerializer,
        'search': employees_s.EmployeeSearchSerializer,
        'destroy': employees_s.EmployeeSearchSerializer,
    }

    lookup_url_kwarg = 'user_id'
    http_method_names = ('get', 'post', 'patch', 'delete',)

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
        )

    def get_queryset(self):
        qs = Employee.objects.select_related(
            'user',
            'category',
            'role',

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

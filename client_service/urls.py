from django.urls import path, include
from rest_framework.routers import DefaultRouter

from client_service.views import sales_view, service_view

router = DefaultRouter()


router.register(r'sales_view', sales_view.SalesView, 'sales_view')
router.register(r'service_view', service_view.ServiceView, 'service_view')

urlpatterns = [
    path('client_service/', include(router.urls)),
]

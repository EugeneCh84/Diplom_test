from django.urls import path, include
from rest_framework.routers import DefaultRouter

from clients import views

router = DefaultRouter()


router.register(r'clients', views.ClientView, 'clients')


urlpatterns = [
    path('clients/', include(router.urls)),
]

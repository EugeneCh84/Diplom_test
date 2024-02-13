from django.urls import path, include
from rest_framework.routers import DefaultRouter

from equipment import views

router = DefaultRouter()


router.register(r'equipment', views.EquipmentView, 'equipment')


urlpatterns = [
    path('equipment/', include(router.urls)),
]

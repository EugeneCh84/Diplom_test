from django.urls import path, include
from rest_framework.routers import DefaultRouter

from staff.views import employee_view, manage_view

router = DefaultRouter()


router.register(r'employees', employee_view.EmployeeView, 'employees')
router.register(r'managers', manage_view.ManagerView, 'managers')

urlpatterns = [
    path('company/', include(router.urls)),
]

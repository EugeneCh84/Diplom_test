from api.spectacular.urls import urlpatterns as doc_urls
from users.urls import urlpatterns as user_urls
from django.urls import path, include
from staff.urls import urlpatterns as staff_urls
from equipment.urls import urlpatterns as equipment_urls
from clients.urls import urlpatterns as clients_urls
from client_service.urls import urlpatterns as client_service_urls
app_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += staff_urls
urlpatterns += equipment_urls
urlpatterns += clients_urls
urlpatterns += client_service_urls

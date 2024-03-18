from django.urls import path
from . import views

urlpatterns = [
    path('listcreate/',views.ListCreateRole.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteRole.as_view(), name='rud'),
    path('listcreatep/',views.ListCreatePermission.as_view(), name='listcreate'),
]
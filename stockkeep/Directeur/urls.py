from django.urls import path
from . import views

urlpatterns = [
    path('listcreate/',views.PermissionList.as_view(), name='listcreate'),

]
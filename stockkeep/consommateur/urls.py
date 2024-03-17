from django.urls import path
from . import views


urlpatterns = [
    path('listcreate/',views.ListCreateCons.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteCons.as_view(), name='delete'),

]
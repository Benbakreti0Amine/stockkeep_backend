from django.urls import path
from . import views


urlpatterns = [
    path('listcreate/',views.ListCreateCons.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteCons.as_view(), name='delete'),
    path('bondecommandeinterne/listcreate/',views.BonDeCommandeInterneCreateView.as_view(), name='bon-listcreate'),
    path('bondecommandeinterne/rud/<int:pk>/',views.BonDeCommandeInterneRUDView.as_view(), name='bon-rud'),

]
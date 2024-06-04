from django.urls import path
from . import views


urlpatterns = [
    path('listcreate/',views.ListCreateCons.as_view(), name='listcreate'),
    path('rud/<int:pk>/',views.RetrieveUpdateDeleteCons.as_view(), name='delete'),
    path('bondecommandeinterne/listcreate/',views.BonDeCommandeInterneCreateView.as_view(), name='bon-listcreate'),
    path('bondecommandeinterne/rud/<int:pk>/',views.BonDeCommandeInterneRUDView.as_view(), name='bon-rud'),
    path('bci_statistics/<int:id>/', views.bci_statistics_for_consommateur, name='bci_statistics_for_consommateur'),
    path('api/commandes/structure/<int:structure_id>/',views.BonDeCommandeInterneByStructureView.as_view(), name='api_commandes_by_structure'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('bondecommandeinterne/rud/<int:pk>/',views.BonDeCommandeInterneRUDView.as_view(), name='bon-rud'),
    path('bondecommandeinterne/list/',views.BonDeCommandeInterneListView.as_view(), name='bonlist'),
    # path('etatinventaire/list/',views.EtatInventaireDirListView.as_view(), name='etatlist'),
    # path('etatinventaire/rud/<int:pk>/',views.EtatInventaireDirRUDView.as_view(), name='etat-rud'),
    path('ticket/list/',views.TicketListView.as_view(), name='ticketlist'),
    path('ticket/list/<int:bon_de_commande_id>/',views.TicketSearchView.as_view(), name='ticketlist'),
]
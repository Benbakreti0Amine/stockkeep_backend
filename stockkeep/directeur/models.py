from django.db import models

from consommateur.models import BonDeCommandeInterne

# Create your models here.
class TicketSuiviCommande(models.Model):
    bon_de_commande = models.ForeignKey(BonDeCommandeInterne, on_delete=models.CASCADE, related_name='tickets')
    etape = models.CharField(max_length=100)
    items = models.JSONField() 

    def __str__(self):
        return f"Ticket {self.id} - {self.etape} - {self.bon_de_commande}"

    @classmethod
    def create_ticket(cls, bon_de_commande, etape, items_info):
        return cls.objects.create(bon_de_commande=bon_de_commande, etape=etape, items=items_info)
from django.db import models
from Service_Achat.models import BonDeCommande



class BonDeReception(models.Model):
    bon_de_commande = models.ForeignKey(BonDeCommande, on_delete=models.CASCADE, related_name='receipts')
    date = models.DateField(auto_now_add=True)
    

    def __str__(self):
        return f"Bon de réception {self.id} - {self.bon_de_commande}"

class BonDeReceptionItem(models.Model):
    bon_de_reception = models.ForeignKey(BonDeReception, on_delete=models.CASCADE, related_name='items')
    # item = models.ForeignKey(Item, on_delete=models.CASCADE)
    nom_produit=models.CharField(max_length=255)
    quantite_commandee = models.PositiveIntegerField(null=True)
    quantite_livree = models.PositiveIntegerField(null=True)
    reste_a_livrer = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):
        self.reste_a_livrer = self.quantite_commandee - self.quantite_livree
        super().save(*args, **kwargs)

    def __str__(self):
        return f" - Commandée: {self.quantite_commandee} - Livrée: {self.quantite_livree}"
    
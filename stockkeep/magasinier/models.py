from django.db import models
from Service_Achat.models import BonDeCommande, Produit
from consommateur.models import BonDeCommandeInterne, BonDeCommandeInterneItem
from django.db import transaction


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
        with transaction.atomic():
            self.reste_a_livrer = self.quantite_commandee - self.quantite_livree
            super().save(*args, **kwargs)

            produit = Produit.objects.get(designation=self.nom_produit)

            # Update produit's stock
            produit.quantite_en_stock += self.quantite_livree
            produit.save()

            # Update related BonDeCommande's Item reste_a_livrer
            item = self.bon_de_reception.bon_de_commande.items.filter(produit__designation=self.nom_produit).first()
            if item:
                item.reste_a_livrer = self.reste_a_livrer
                item.save()

            # Check if all related items have been delivered
            if self.bon_de_reception.items.filter(reste_a_livrer__gt=0).exists():
                self.bon_de_reception.bon_de_commande.status = 'pending'
            else:
                self.bon_de_reception.bon_de_commande.status = 'completed'

            self.bon_de_reception.bon_de_commande.save()

    def __str__(self):
        return f" - Commandée: {self.quantite_commandee} - Livrée: {self.quantite_livree}"
    


class BonDeSortie(models.Model):
    bon_de_commande_interne = models.ForeignKey(BonDeCommandeInterne, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    TYPE_CHOICES = (
        ('Supply', 'Supply'),
        ('Decharge', 'Decharge'),

    )
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)


class BonDeSortieItem(models.Model):
    bon_de_sortie = models.ForeignKey(BonDeSortie, related_name='items', on_delete=models.CASCADE)
    bon_de_commande_interne_item = models.ForeignKey(BonDeCommandeInterneItem,related_name='bondesortie_item', on_delete=models.CASCADE)
    quantite_accorde=models.IntegerField()
    observation = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # If the type is "Decharge", subtract quantite_accorde from quantite_en_stock of Produit
            if self.bon_de_sortie.type == 'Supply':
                # Retrieve the associated Produit
                produit = self.bon_de_commande_interne_item.produit

                # Subtract quantite_accorde from quantite_en_stock of Produit
                produit.quantite_en_stock -= self.quantite_accorde
                produit.save()

        # Call save method of the superclass
        super().save(*args, **kwargs)

class EtatInventaire(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    ETAT_CHOICES = (
        ('Approuved', 'Approuved'),
        ('Not Approuved', 'Non Approuved'),

    )
    etat = models.CharField(max_length=100,choices=ETAT_CHOICES)
    produits = models.ManyToManyField('EtatInventaireProduit')


class EtatInventaireProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_physique = models.IntegerField(default=0)
    observation = models.TextField(blank=True)
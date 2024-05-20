from django.db import models
from Service_Achat.models import BonDeCommande, Produit,Chapitre,Article
from consommateur.models import BonDeCommandeInterne, BonDeCommandeInterneItem
from users.models import User
from django.db import transaction
from datetime import date


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
    # date = models.DateField(default=date(2024, 4, 3))
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
        
        super().save(*args, **kwargs)

        with transaction.atomic():
            # If the type is "Decharge", subtract quantite_accorde from quantite_en_stock of Produit
            if self.bon_de_sortie.type == 'Supply':
                # Retrieve the associated Produit
                produit = self.bon_de_commande_interne_item.produit

                # Subtract quantite_accorde from quantite_en_stock of Produit
                produit.quantite_en_stock -= self.quantite_accorde
                produit.save()

class EtatInventaire(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    ETAT_CHOICES = (
        ('Approuved', 'Approuved'),
        ('Not Approuved', 'Non Approuved'),

    )
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE, related_name='etat_inventaires_chap')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='etat_inventaires_art')
    etat = models.CharField(max_length=150,choices=ETAT_CHOICES)
    produits = models.ManyToManyField('EtatInventaireProduit',related_name="etatinventaire")


class EtatInventaireProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE,related_name='produ')
    N_inventaire = models.CharField(max_length=255)
    reste = models.IntegerField(default=0)
    quantite_entree = models.IntegerField(default=0)
    quantite_sortie = models.IntegerField(default=0)
    quantite_physique = models.IntegerField(default=0)
    quantite_logique = models.IntegerField(default=0)
    observation = models.TextField(blank=True)
    ecrat = models.IntegerField(blank=True)

    def save(self, *args, **kwargs):
        """Overrides the default save method to calculate difference."""
        self.ecrat = self.quantite_logique - self.quantite_physique  
        super().save(*args, **kwargs) 


class AdditionalInfo(models.Model):
    numero_bon = models.CharField(max_length=255, null=True, blank=True)
    quantite_sortie = models.IntegerField(null=True, blank=True)
    consommateur = models.CharField(max_length=255, null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    date_sortie = models.DateField(null=True, blank=True)

class FicheMovement(models.Model):
    produit_id = models.IntegerField()  # ID of the related product
    date_entree = models.DateField(null=True, blank=True)
    fournisseur = models.CharField(max_length=255, blank=True)
    quantite_entree = models.IntegerField(null=True, blank=True)
    sum_quantite_sortie = models.IntegerField(null=True, blank=True)
    reste = models.IntegerField(null=True, blank=True)
    additional_info = models.ManyToManyField(AdditionalInfo, blank=True)


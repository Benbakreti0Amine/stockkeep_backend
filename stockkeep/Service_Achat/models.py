from django.db import models
from fournisseur.models import Fournisseur
from functools import partial
class Chapitre(models.Model):
    libelle = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.libelle

class Article(models.Model):
    designation = models.CharField(max_length=255,unique=True)
    chapitre = models.ForeignKey(Chapitre, related_name='articles', on_delete=models.CASCADE)
    tva = models.DecimalField(max_digits=10, decimal_places=2, default=19)

    def __str__(self):
        return self.designation

class Produit(models.Model):
    designation = models.CharField(max_length=255,unique=True)
    articles = models.ManyToManyField(Article, related_name='produits')
    quantite_en_stock = models.IntegerField(default=0)
    quantite_en_security = models.IntegerField(default=0)


    def __str__(self):
        return self.designation
    

class Item(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    reste_a_livrer = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):
        # Calculate the amount
        self.montant = self.prix_unitaire * self.quantite
        if not self.pk:  # Check if it's a new instance
            self.reste_a_livrer = self.quantite  # Only update reste_a_livrer on creation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit} - {self.quantite}"
    

    

class BonDeCommande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item)  # Change ForeignKey to ManyToManyField
    tva = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    montant_global = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    

    def __str__(self):
        return f"Commande {self.id} - {self.fournisseur} - {self.date}"


# class ItemReceived(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     # bon_de_reception = models.ForeignKey(BonDeReception, on_delete=models.CASCADE, related_name='items_received')
#     quantite_livree = models.PositiveIntegerField()
#     reste_a_livrer = models.PositiveIntegerField(default=0)  # Automatically calculated based on the quantity ordered

#     def save(self, *args, **kwargs):
#             self.reste_a_livrer = self.item.quantite - self.quantite_livree
#             super().save(*args, **kwargs)



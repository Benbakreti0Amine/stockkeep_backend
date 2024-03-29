from django.db import models
from fournisseur.models import Fournisseur
class Chapitre(models.Model):
    libelle = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.libelle

class Article(models.Model):
    designation = models.CharField(max_length=255,unique=True)
    chapitre = models.ForeignKey(Chapitre, related_name='articles', on_delete=models.CASCADE)

    def __str__(self):
        return self.designation

class Produit(models.Model):
    designation = models.CharField(max_length=255,unique=True)
    article = models.ForeignKey(Article, related_name='produits', on_delete=models.CASCADE)

    def __str__(self):
        return self.designation

class Item(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calculate the amount
        self.montant = self.prix_unitaire * self.quantite
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.produit} - {self.quantite}"

class BonDeCommande(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    items = models.ForeignKey(Item,on_delete=models.SET_NULL,null=True)   
    tva = models.DecimalField(max_digits=10, decimal_places=2)
    montant_global = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # def save(self, *args, **kwargs):
    #     # Calculate the total amount including VAT
    #     self.montant_global = sum(item.montant for item in self.items.all()) + (sum(item.montant for item in self.items.all()) * self.tva / 100)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande {self.id} - {self.fournisseur} - {self.date}"
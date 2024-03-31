from django.db import models
from fournisseur.models import Fournisseur
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
    article = models.ForeignKey(Article, related_name='produits', on_delete=models.CASCADE)

    def __str__(self):
        return self.designation

class Item(models.Model):
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    quantite = models.PositiveIntegerField()
    montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Calculate the amount
        self.montant = self.prix_unitaire * self.quantite
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
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    

    def __str__(self):
        return f"Commande {self.id} - {self.fournisseur} - {self.date}"
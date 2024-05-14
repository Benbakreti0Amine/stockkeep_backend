from django.db import models
from users.models import User
from structure.models import Structure
from Service_Achat.models import Produit

from django.contrib.auth.models import  BaseUserManager
# Create your models here.
class MyUserManager(BaseUserManager):

    def create_user(self, username, email,first_name,last_name, password, **kwags):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a firstname')
        if not last_name:
            raise ValueError('Users must have a lastname')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.is_active  = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Consommateur(User):
    structure = models.ForeignKey(Structure,on_delete=models.SET_NULL,null=True,related_name='consommateurs')


class BonDeCommandeInterneItem(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite_demandee = models.PositiveIntegerField(null=True)
    quantite_accorde = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"{self.produit} - {self.quantite_demandee}"

class BonDeCommandeInterne(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bonDeiommandeinternes')
    date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('Created succesfully', 'Created succesfully'),
        ('Consulted by the responsable', 'Consulted by the responsable'),
        ('Consulted by the director', 'Consulted by the director'),
        ('Delivered', 'Delivered'),
        ('External Discharge', 'External Discharge'),
    )
    TYPE_CHOICES = (
        ('Supply', 'Supply'),
        ('Decharge', 'Decharge'),
    )
    status = models.CharField(max_length=40, choices=STATUS_CHOICES)
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)
    items = models.ManyToManyField(BonDeCommandeInterneItem)

    def __str__(self):
        return f"Commande {self.id} - {self.user_id} - {self.date}"


    
    
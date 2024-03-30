from django.db import models

class Fournisseur(models.Model):
    raison_sociale = models.CharField(max_length=255, verbose_name="Raison sociale")
    adresse = models.CharField(max_length=255, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    fax = models.CharField(max_length=20, verbose_name="Fax")
    num_registre_commerce = models.CharField(max_length=20, verbose_name="N° Registre Commerce")
    rib_ou_rip = models.CharField(max_length=20, verbose_name="RIB (ou RIP)")
    nif = models.IntegerField(verbose_name="N° Identification Fiscale")
    nis = models.IntegerField(verbose_name="Numéro d'identification statistique")

    def __str__(self):
        return self.raison_sociale
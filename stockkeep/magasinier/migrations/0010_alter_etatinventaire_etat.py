# Generated by Django 4.2.4 on 2024-05-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinier', '0009_remove_etatinventaireproduit_etat_inventaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='etatinventaire',
            name='etat',
            field=models.CharField(choices=[('Approuved', 'Approuved'), ('Not Approuved', 'Non Approuved')], max_length=100),
        ),
    ]

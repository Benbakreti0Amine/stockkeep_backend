# Generated by Django 4.2.4 on 2024-04-22 14:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Service_Achat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonDeReception',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('bon_de_commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to='Service_Achat.bondecommande')),
            ],
        ),
        migrations.CreateModel(
            name='BonDeReceptionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=255)),
                ('quantite_commandee', models.PositiveIntegerField()),
                ('quantite_livree', models.PositiveIntegerField()),
                ('reste_a_livrer', models.DecimalField(blank=True, decimal_places=2, max_digits=10)),
                ('bon_de_reception', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='magasinier.bondereception')),
            ],
        ),
    ]

# Generated by Django 4.2.4 on 2024-04-28 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consommateur', '0004_bondecommandeinterneitem_quantite_accorde'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bondecommandeinterne',
            name='status',
            field=models.CharField(choices=[('transfert', 'Transfert'), ('responsable', 'Responsable'), ('dircteur', 'Dircteur'), ('validate', 'Validate')], max_length=20),
        ),
    ]
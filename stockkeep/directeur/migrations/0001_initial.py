# Generated by Django 4.2.4 on 2024-05-20 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('consommateur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSuiviCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etape', models.CharField(max_length=100)),
                ('items', models.JSONField()),
                ('bon_de_commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='consommateur.bondecommandeinterne')),
            ],
        ),
    ]

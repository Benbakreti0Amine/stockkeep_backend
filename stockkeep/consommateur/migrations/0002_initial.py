# Generated by Django 4.2.4 on 2024-05-07 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('structure', '0001_initial'),
        ('Service_Achat', '0001_initial'),
        ('consommateur', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consommateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('structure', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consommateurs', to='structure.structure')),
            ],
            options={
                'abstract': False,
            },
            bases=('users.user',),
        ),
        migrations.AddField(
            model_name='bondecommandeinterneitem',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Service_Achat.produit'),
        ),
        migrations.AddField(
            model_name='bondecommandeinterne',
            name='Consommateur_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bonDeiommandeinternes', to='consommateur.consommateur'),
        ),
        migrations.AddField(
            model_name='bondecommandeinterne',
            name='items',
            field=models.ManyToManyField(to='consommateur.bondecommandeinterneitem'),
        ),
    ]

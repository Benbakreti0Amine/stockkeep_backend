# Generated by Django 4.2.4 on 2024-04-30 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consommateur', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bondecommandeinterne',
            name='status',
            field=models.CharField(choices=[('Created succesfully', 'Created succesfully'), ('Consulted by the responsable', 'Consulted by the responsable'), ('Consulted by the director', 'Consulted by the director'), ('Validate', 'Validate')], max_length=40),
        ),
    ]
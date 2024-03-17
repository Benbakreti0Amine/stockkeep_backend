# Generated by Django 5.0.3 on 2024-03-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structure',
            name='abbreviation',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='structure',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]

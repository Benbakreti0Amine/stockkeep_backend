# Generated by Django 4.2.4 on 2024-05-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]

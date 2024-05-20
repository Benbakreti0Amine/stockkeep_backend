# Generated by Django 4.2.4 on 2024-05-20 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('structure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='structure',
            name='responsible',
            field=models.ForeignKey(limit_choices_to={'role__name': 'responsable_structure'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resposable', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2.4 on 2024-05-14 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_role_alter_notification_recipient'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='titre',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

# Generated by Django 2.0.6 on 2019-10-04 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RedesApp', '0002_auto_20191004_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='mqttdef',
            name='mensajes_minuto',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='mqttdef',
            name='cant_mensajes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

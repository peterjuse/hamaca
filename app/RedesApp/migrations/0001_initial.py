# Generated by Django 2.0.6 on 2019-10-04 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MQTTdef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('sensor', models.CharField(max_length=75)),
                ('variable', models.CharField(max_length=75)),
                ('valor', models.TextField()),
                ('hora', models.CharField(max_length=28)),
            ],
        ),
    ]
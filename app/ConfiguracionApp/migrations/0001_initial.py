# Generated by Django 2.0.6 on 2019-08-30 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='variables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='El nombre de la variable global de la aplicacion', max_length=50)),
                ('valor', models.TextField()),
            ],
        ),
    ]
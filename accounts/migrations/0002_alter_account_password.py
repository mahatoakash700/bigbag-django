# Generated by Django 4.2.2 on 2023-07-11 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(default='', max_length=10),
        ),
    ]
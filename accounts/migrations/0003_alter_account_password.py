# Generated by Django 4.2.2 on 2023-07-11 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]

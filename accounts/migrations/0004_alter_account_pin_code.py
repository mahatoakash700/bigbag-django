# Generated by Django 4.2.2 on 2023-07-11 11:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pin_code',
            field=models.CharField(default=751001, max_length=6, null=True, validators=[django.core.validators.MinLengthValidator(6), django.core.validators.MaxLengthValidator(6)]),
        ),
    ]

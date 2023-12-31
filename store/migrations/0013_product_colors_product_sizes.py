# Generated by Django 4.2.2 on 2023-06-27 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_delete_productvariant'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(to='store.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]

# Generated by Django 4.2.2 on 2023-06-25 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_product_name_product_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='name',
            new_name='product_name',
        ),
    ]

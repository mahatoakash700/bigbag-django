# Generated by Django 4.2.2 on 2023-06-25 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_product_color_available_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductVariant',
        ),
    ]

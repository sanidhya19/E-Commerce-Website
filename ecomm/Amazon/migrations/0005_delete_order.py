# Generated by Django 5.1.6 on 2025-03-28 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Amazon', '0004_remove_order_address_remove_order_phone_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]

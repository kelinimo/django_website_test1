# Generated by Django 5.0.3 on 2024-03-26 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_products_new_order_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]

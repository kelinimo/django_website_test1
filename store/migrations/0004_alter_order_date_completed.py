# Generated by Django 5.0.3 on 2024-03-26 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_rename_orderitem_orderproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_completed',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

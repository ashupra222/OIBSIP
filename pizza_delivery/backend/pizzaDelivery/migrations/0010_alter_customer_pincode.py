# Generated by Django 4.1.13 on 2024-06-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaDelivery', '0009_customer_alter_order_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='pincode',
            field=models.PositiveIntegerField(null=True),
        ),
    ]

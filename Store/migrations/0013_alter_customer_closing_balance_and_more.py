# Generated by Django 4.0.2 on 2023-10-06 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0012_customer_closing_balance_customer_opening_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='closing_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='customer',
            name='opening_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='milkcenter',
            name='closing_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='milkcenter',
            name='opening_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

# Generated by Django 4.0.2 on 2023-10-05 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_storage_remove_customer_branch_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
    ]
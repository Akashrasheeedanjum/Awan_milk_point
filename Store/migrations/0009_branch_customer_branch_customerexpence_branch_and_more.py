# Generated by Django 4.0.2 on 2023-10-02 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0008_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('contact', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='customerexpence',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='expence',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='makepayment',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='milkcenter',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='milkpurchase',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='milksale',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='receivedpayment',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
        migrations.AddField(
            model_name='stor',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='Store.branch'),
        ),
    ]

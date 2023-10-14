# Generated by Django 4.0.2 on 2023-10-11 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0015_remove_branch_user_remove_branch_user_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
        migrations.AddField(
            model_name='milkcenter',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]

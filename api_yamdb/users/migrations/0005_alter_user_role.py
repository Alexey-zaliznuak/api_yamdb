# Generated by Django 3.2 on 2023-03-03 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20230303_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'Authenticated user'), ('moderator', 'Moderator'), ('admin', 'Administrator')], default='user', max_length=16, verbose_name='user role'),
        ),
    ]
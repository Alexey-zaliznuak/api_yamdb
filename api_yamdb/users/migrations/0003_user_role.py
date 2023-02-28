# Generated by Django 3.2 on 2023-02-28 12:51

from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, default=users.models.get_user_default_role, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Users_with_this_role', to='users.role', verbose_name='User Role'),
        ),
    ]
